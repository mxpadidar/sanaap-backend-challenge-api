from django.conf import settings
from django.db import models

from sanaap.docs.enums import DocStatus


class Document(models.Model):
    uuid = models.UUIDField(db_index=True)
    bucket = models.CharField(max_length=255, default=settings.DOCS_BUCKET, db_index=True)
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    mimetype = models.CharField(max_length=255)
    etag = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=16,
        choices=DocStatus.choices,
        default=DocStatus.ACTIVE,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logs = models.JSONField(default=dict, blank=True)

    class Meta:
        default_permissions = ("read", "write", "delete")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["uuid", "status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["uuid"],
                condition=models.Q(status=DocStatus.ACTIVE),
                name="uniq_active_uuid",
            ),  # uuid should be unique among active documents
            models.UniqueConstraint(
                fields=["bucket", "name"],
                condition=models.Q(status=DocStatus.ACTIVE),
                name="uniq_active_doc_name",
            ),  # name should be unique in a bucket among active documents
        ]

    def __str__(self) -> str:
        return f"{self.name}: {self.status}"
