import sys
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from gl_site.models import Organization
from gl_site.test.factory import Factory

from gl_site.inventories import inventory_cls_list as all_inventory_classes
from gl_site.inventories.big_five import BigFive
from gl_site.inventories.core_self import CoreSelf
from gl_site.inventories.career_commitment import CareerCommitment
from gl_site.inventories.ambiguity import Ambiguity
from gl_site.inventories.via import Via

class Command(BaseCommand):
    """
    This was created for testing the statistics features. It could be
    good for other things too.

    Don't run this command when there is real (i.e. important) information
    in the database.

    Additional documentation:
    https://github.com/srmagura/goodnight-lead/wiki/Management-commands
    """

    help = 'Create a lot of fake organizations, sessions, users, .etc'

    def handle(self, **options):
        # Delete what was there before so we have a clean start
        User.objects.filter(username='testadmin0').delete()
        User.objects.filter(username__startswith='testuser').delete()

        admin = Factory.create_admin()

        # Typical-case organization
        chess = Factory.create_organization(admin, name='UNC Chess Club')
        chess_session = Factory.create_session(chess, admin, name='Fall 2016')
        self.add_users(chess_session, 10)

        # Orgainization with two sessions
        strawhats = Factory.create_organization(admin, name='Strawhats')
        strawhats_session1 = Factory.create_session(strawhats, admin,
            name='East Blue')
        self.add_users(strawhats_session1, 9)
        strawhats_session2 = Factory.create_session(strawhats, admin,
            name='Grand Line')
        self.add_users(strawhats_session2, 11)

        # Organization where not everyone has completed all of the inventories
        incomplete = Factory.create_organization(admin, name='Incompletionists')
        incomplete_session = Factory.create_session(incomplete, admin, name='Fall 2016')

        for i in range(10):
            # Everyone completes BigFive
            inventory_cls_list = [BigFive]

            # 9 users complete CoreSelf
            if i != 9:
                inventory_cls_list.append(CoreSelf)

            # 2 users complete CareerCommitment
            if i < 2:
                inventory_cls_list.append(CareerCommitment)

            # 1 user completes Ambiguity and Via
            if i == 0:
                inventory_cls_list.append(Ambiguity)
                inventory_cls_list.append(Via)

            # No one completes FIRO-B or Via

            self.add_user(incomplete_session, inventory_cls_list)

        print()

    def add_users(self, session, n_user,
        inventory_cls_list=all_inventory_classes):
        for i in range(n_user):
            self.add_user(session, inventory_cls_list)

    def add_user(self, session, inventory_cls_list):
        user, info = Factory.create_user(session)
        Factory.create_set_of_submissions(user, inventory_cls_list)

        print('.', end='')
        sys.stdout.flush()
