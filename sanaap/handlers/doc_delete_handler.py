import datetime
import logging
import uuid

from sanaap import exceptions
from sanaap.docs.enums import DocStatus
from sanaap.docs.models import Document
from sanaap.services.storage_service import MinioStorage

logger = logging.getLogger(__name__)


def handle_document_delete(
    storage: MinioStorage, file_uuid: uuid.UUID, username: str
) -> None:
    doc = Document.objects.filter(uuid=file_uuid, status=DocStatus.ACTIVE).first()
    if doc is None:
        raise exceptions.NotFoundExc("document not found.")
    doc.status = DocStatus.DELETED
    doc.logs = doc.logs or {}
    doc.logs.update(
        {
            "deleted_by": username,
            "deleted_at": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        }
    )
    doc.save(update_fields=["status", "logs"])
    storage.delete(bucket=doc.bucket, name=doc.name)
    logger.info(f"document {file_uuid} deleted by user {username}")
