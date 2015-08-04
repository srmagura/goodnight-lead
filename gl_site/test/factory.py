# gl_site models
from gl_site.models import Organization, Session, LeadUserInfo, Submission

# Django User
from django.contrib.auth.models import User

# Date utilities
from datetime import date

# Inventories
from gl_site.inventories import inventory_cls_list
from .statistics.inventory_answers import inventory_data

class Factory:
    """ Factory class for creating commonly used objects in testing """

    index = 0
    default_password = 'password'

    @classmethod
    def increment_index(cls):
        """ Increment the factory index. Guarantees uniqueness. """
        cls.index = cls.index + 1

    @classmethod
    def create_organization(cls, created_by):
        """ Create an organization and set the creating user """

        org = Organization.objects.create(
            name = "Test Organization {}".format(cls.index),
            code = "Secret {}".format(cls.index),
            created_by = created_by
        )
        cls.increment_index()
        return org

    @classmethod
    def create_session(cls, organization, created_by):
        """ Create a session and set the organization and creating user """

        session = Session.objects.create(
            name = "Test Session {}".format(cls.index),
            organization = organization,
            created_by = created_by
        )
        cls.increment_index()
        return session

    @classmethod
    def create_user(cls, session=None):
        """
        Create a default user, including its LeadUserInfo, Organization,
        and Session.

        If a session argument is provided, the user will be placed in
        the session and its organization. No new organization or session
        is created.
        """
        user = User.objects.create_user(
            username = "testuser{}".format(cls.index),
            email = "testuser{}@gmail.com".format(cls.index),
            password = cls.default_password,
            first_name = "test{}".format(cls.index),
            last_name = "user{}".format(cls.index)
        )

        if session is None:
            organization = cls.create_organization(user)
            session = cls.create_session(organization, user)
        else:
            organization = session.organization

        info = LeadUserInfo.objects.create(
            user = user,
            gender = 'M',
            major = LeadUserInfo.OTHER,
            education = 'FR',
            graduation_date = date.today(),
            organization = organization,
            session = session
        )

        cls.increment_index()
        return (user, info)

    @classmethod
    def create_admin(cls):
        """
        Create and return a superuser.

        Note that the superuser does not have an associated LeadUserInfo.
        This is the case for superusers created via manage.py
        createsuperuser.
        """
        admin = User.objects.create_superuser(
            "testadmin{}".format(cls.index),
            "testadmin{}@gmail.com".format(cls.index),
            cls.default_password,
        )

        return admin

    @classmethod
    def create_user_settings_post_dict(cls, user, leaduserinfo):
        """ Create the dictionary sent through post for account settings """

        return {
            # User fields
            'username': user.username,
            'email': user.email,
            'password': cls.default_password,
            'first_name': user.first_name,
            'last_name': user.last_name,

            # Info fields
            'gender': leaduserinfo.gender,
            'major': leaduserinfo.major,
            'education': leaduserinfo.education,
            'graduation_date': leaduserinfo.graduation_date,
        }

    @classmethod
    def create_user_registration_post_dict(cls, organization):
        """ Create a registration dict
            Returns a registration dictionary with unique
            user information where applicable.
        """

        form =  {
            # User fields
            'username' : "testuser{}".format(cls.index),
            'email' : "testuser{}@gmail.com".format(cls.index),
            'password1' : cls.default_password,
            'password2' : cls.default_password,
            'first_name' : "test{}".format(cls.index),
            'last_name' : "user{}".format(cls.index),

            # Info fields
            'gender': 'M',
            'major': LeadUserInfo.OTHER,
            'education': 'FR',
            'graduation_date' : str(date.today()),
            'organization_code' : organization.code
        }
        cls.increment_index()
        return form

    @classmethod
    def create_set_of_submissions(cls, user):
        """ Generate and save a single set of submissions for each inventory """
        for inventory_cls in inventory_cls_list:
            # Create an inventory
            inventory =  inventory_cls()

            # Generate the submission
            submission = Submission()
            submission.inventory_id = inventory.inventory_id
            submission.user = user
            submission.current_page = inventory.n_pages - 1
            submission.save()
            inventory.set_submission(submission)

            # Set answers and compute metrics
            answers = inventory_data[inventory_cls.__name__]['answers']
            cls.set_answers(inventory, answers)
            inventory.compute_metrics()

            # Save the metrics
            inventory.save_metrics()

    @classmethod
    def set_answers(cls, inv, answers):
        """ Imports provided answers into an inventory's
            answers dictionary.

            Inputs:
            inv     - Instance of Inventory which the answers will be
                      imported to.
            answers - Set of pre-defined answers for an inventory.

        """
        if type(answers) is dict:
            inv.answers = answers
        else:
            inv.answers = {}
            i = 1
            for answer in answers:
                inv.answers[i] = answer
                i += 1
