import io

import pytest

from sanaap.docs.models import Document
from sanaap.handlers import handle_document_upload
from sanaap.services import MinioStorage

pytestmark = pytest.mark.django_db


def test_handler_creates_document_with_valid_data(storage: MinioStorage):
    data = {
        "username": "test-user",
        "bucket": "test-bucket",
        "file": io.BytesIO(b"test file content"),
        "name": "test.txt",
        "size": 17,
        "ext": "txt",
        "mimetype": "text/plain",
    }

    doc = handle_document_upload(storage=storage, **data)
    assert isinstance(doc, Document)
    assert doc.uuid is not None
    assert doc.bucket == data["bucket"]
    assert doc.name.endswith(".txt")
    assert doc.size == data["size"]
    assert doc.mimetype == data["mimetype"]
    assert doc.status == "active"
    assert doc.logs == {"uploaded_by": data["username"]}
    assert Document.objects.filter(uuid=doc.uuid).exists()
