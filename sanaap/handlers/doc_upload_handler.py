import io
import uuid
from typing import TypedDict, Unpack

from sanaap.docs.models import Document
from sanaap.services import MinioStorage


class UploadData(TypedDict):
    username: str
    bucket: str
    file: io.BytesIO
    name: str
    size: int
    ext: str
    mimetype: str


def handle_document_upload(storage: MinioStorage, **data: Unpack[UploadData]) -> Document:
    file_uuid = uuid.uuid4()
    unique_name = f"{file_uuid.hex}.{data['ext']}"

    result = storage.upload(
        file=data["file"],
        bucket=data["bucket"],
        name=unique_name,
        size=data["size"],
    )

    doc = Document.objects.create(
        uuid=file_uuid,
        bucket=data["bucket"],
        name=unique_name,
        size=data["size"],
        mimetype=data["mimetype"],
        etag=result["etag"],
        logs={"uploaded_by": data["username"]},
    )

    return doc
