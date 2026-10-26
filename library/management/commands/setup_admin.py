from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates or resets the default admin superuser (admin / admin123)"

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@library.local',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        user.set_password('admin123')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Successfully created admin superuser (admin / admin123)"))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully reset admin password to 'admin123' (active: True)"))
