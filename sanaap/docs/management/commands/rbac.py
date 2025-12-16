import logging

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

logger = logging.getLogger("sanaap.auth")


class Command(BaseCommand):
    help = "Create document permissions and groups"

    def handle(self, *args, **kwargs) -> None:
        dct = ContentType.objects.get(app_label="docs", model="document")

        rp = Permission.objects.get(content_type=dct, codename="read_document")
        wp = Permission.objects.get(content_type=dct, codename="write_document")
        dp = Permission.objects.get(content_type=dct, codename="delete_document")

        group_perms = {"normal": [rp], "staff": [rp, wp], "admin": [rp, wp, dp]}

        for name, perms in group_perms.items():
            group, created = Group.objects.get_or_create(name=name)
            group.permissions.set(perms)
            if created:
                logger.info(f"{group.name=} created.")
                group.permissions.set(perms)
                logger.info(f"{[p.codename for p in perms]} assigned to group")
            else:
                logger.info(f"{group.name=} already exists")
