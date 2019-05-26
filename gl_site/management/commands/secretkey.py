"""Utility for generating a new secret key."""


# Imports
from django.core.management import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    """Secret key command."""

    def handle(self, *args, **options):
        self.stdout.write(get_random_secret_key())
