from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Seeds the database with test users (admin and newuser)'

    def handle(self, *args, **options):
        # Create admin user
        try:
            admin = User.objects.create_user(
                username='admin',
                password='2025DEVChallenge',
                email='admin@example.com',
                is_staff=True,  # Admin privileges
                is_superuser=True  # Superuser privileges
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create newuser (member)
        try:
            newuser = User.objects.create_user(
                username='newuser',
                password='2025DEVChallenge',
                email='newuser@example.com',
                is_staff=False,  # Regular user
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS('Successfully created newuser'))
        except IntegrityError:
            self.stdout.write(self.style.WARNING('newuser already exists'))