import logging

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

logger = logging.getLogger("sanaap.auth")


class Command(BaseCommand):
    help = "Create default users"

    ADMIN_CREDS = {"username": "admin", "password": "admin"}
    STAFF_CREDS = {"username": "staff", "password": "staff", "is_staff": True}
    NORMAL_CREDS = {"username": "normal", "password": "normal"}

    def handle(self, *args, **kwargs) -> None:
        REQUIRED_GROUPS = {"admin", "staff", "normal"}
        groups = {g.name: g for g in Group.objects.filter(name__in=REQUIRED_GROUPS)}
        missing = REQUIRED_GROUPS - groups.keys()
        if missing:
            raise RuntimeError(f"Required groups are missing: {missing}")

        if not User.objects.filter(username=self.ADMIN_CREDS["username"]).exists():
            admin = User.objects.create_superuser(**self.ADMIN_CREDS)
            admin.groups.add(groups["admin"])
            logger.info("admin user created and added to 'admin' group")
        else:
            logger.info("admin user already exists")

        if not User.objects.filter(username=self.STAFF_CREDS["username"]).exists():
            staff = User.objects.create_user(**self.STAFF_CREDS)
            staff.groups.add(groups["staff"])
            logger.info("staff user created and added to 'staff' group")
        else:
            logger.info("staff user already exists")

        if not User.objects.filter(username=self.NORMAL_CREDS["username"]).exists():
            normal = User.objects.create_user(**self.NORMAL_CREDS)
            normal.groups.add(groups["normal"])
            logger.info("normal user created and added to 'normal' group")
        else:
            logger.info("normal user already exists")
