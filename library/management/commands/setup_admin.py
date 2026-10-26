from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates default superusers (admin/admin123 and yug/yug)"

    def handle(self, *args, **options):
        User = get_user_model()
        
        # User 1: admin
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@library.local', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()

        # User 2: yug
        yug_user, _ = User.objects.get_or_create(
            username='yug',
            defaults={'email': 'yug@library.local', 'is_staff': True, 'is_superuser': True}
        )
        yug_user.set_password('yug')
        yug_user.is_staff = True
        yug_user.is_superuser = True
        yug_user.is_active = True
        yug_user.save()

        self.stdout.write(self.style.SUCCESS("Superusers 'admin' and 'yug' ready!"))
