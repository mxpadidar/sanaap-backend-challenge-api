import io
import logging
import uuid
from datetime import UTC, datetime
from typing import TypedDict, Unpack

from sanaap import exceptions
from sanaap.docs.enums import DocStatus
from sanaap.docs.models import Document
from sanaap.services.storage_service import MinioStorage

logger = logging.getLogger(__name__)


class UploadData(TypedDict):
    username: str
    file_uuid: uuid.UUID
    file: io.BytesIO
    bucket: str
    name: str
    ext: str
    size: int
    mimetype: str


def handle_document_modify(storage: MinioStorage, **data: Unpack[UploadData]) -> Document:
    current_doc = Document.objects.filter(
        uuid=data["file_uuid"], status=DocStatus.ACTIVE
    ).first()
    if current_doc is None:
        raise exceptions.NotFoundExc("document not found.")
    current_doc.status = DocStatus.MODIFIED
    current_doc.logs = current_doc.logs or {}
    current_doc.logs.update(
        {
            "modified_by": data["username"],
            "modified_at": datetime.now(tz=UTC).isoformat(),
        }
    )
    current_doc.save(update_fields=["logs"])
    current_doc.save(update_fields=["status", "logs"])

    # upload new file and create new document record
    unique_name = f"{uuid.uuid4().hex}.{data['ext']}"

    result = storage.upload(
        file=data["file"],
        bucket=data["bucket"],
        name=unique_name,
        size=data["size"],
    )

    doc = Document.objects.create(
        uuid=data["file_uuid"],
        bucket=data["bucket"],
        name=unique_name,
        size=data["size"],
        mimetype=data["mimetype"],
        etag=result["etag"],
        logs={
            "uploaded_by": data["username"],
            "uploaded_at": datetime.now(tz=UTC).isoformat(),
        },
    )

    storage.delete(bucket=current_doc.bucket, name=current_doc.name)

    return doc
