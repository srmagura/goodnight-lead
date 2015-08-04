import sys
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from gl_site.models import Organization
from gl_site.test.factory import Factory

class Command(BaseCommand):
    """
    This was created for testing the statistics features. It could be
    good for other things too.

    Don't run this command when there is real (i.e. important) information
    in the database.
    """

    help = 'Create a lot of fake organizations, sessions, users, .etc'

    def handle(self, **options):
        # Delete what was there before so we have a clean start
        User.objects.filter(username='testadmin0').delete()
        User.objects.filter(username__startswith='testuser').delete()

        admin = Factory.create_admin()

        chess = Factory.create_organization(admin, name='UNC Chess Club')
        chess_session = Factory.create_session(chess, admin, name='Fall 2016')
        self.add_users(chess_session, 10)

        strawhats = Factory.create_organization(admin, name='Strawhats')
        strawhats_session1 = Factory.create_session(strawhats, admin,
            name='East Blue')
        self.add_users(strawhats_session1, 9)
        strawhats_session2 = Factory.create_session(strawhats, admin,
            name='Grand Line')
        self.add_users(strawhats_session2, 11)
        
        print()

    def add_users(self, session, n_user):
        for i in range(n_user):
            self.add_user(session)


    def add_user(self, session):
        user, info = Factory.create_user(session)
        Factory.create_set_of_submissions(user)

        print('.', end='')
        sys.stdout.flush()
