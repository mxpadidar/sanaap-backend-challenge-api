import io
import uuid

import pytest

from sanaap.docs.models import Document
from sanaap.exceptions import NotFoundExc
from sanaap.handlers import handle_document_modify
from sanaap.services import MinioStorage

pytestmark = pytest.mark.django_db


def test_modify_existing_document_add_new_db_record(
    storage: MinioStorage, sample_doc: Document
):
    data = {
        "username": "update-user",
        "file_uuid": sample_doc.uuid,
        "file": io.BytesIO(b"modified content"),
        "bucket": "test-bucket",
        "name": "updated.txt",
        "ext": "txt",
        "size": 16,
        "mimetype": "text/plain",
    }
    modified = handle_document_modify(storage=storage, **data)
    assert isinstance(modified, Document)
    assert modified.uuid == sample_doc.uuid
    assert modified.bucket == data["bucket"]
    assert modified.name.endswith(".txt")
    assert modified.size == data["size"]
    assert modified.mimetype == data["mimetype"]
    assert modified.status == "active"
    assert "uploaded_by" in modified.logs
    assert modified.logs["uploaded_by"] == data["username"]

    # Check old doc is modified
    sample_doc.refresh_from_db()
    assert sample_doc.status == "modified"
    assert "modified_by" in sample_doc.logs
    assert sample_doc.logs["modified_by"] == data["username"]


def test_handler_raises_not_found_for_non_existing_uuid(storage: MinioStorage):
    data = {
        "username": "update-user",
        "file_uuid": uuid.uuid4(),
        "file": io.BytesIO(b"updated content"),
        "bucket": "test-bucket",
        "name": "updated.txt",
        "ext": "txt",
        "size": 15,
        "mimetype": "text/plain",
    }
    with pytest.raises(NotFoundExc):
        handle_document_modify(storage=storage, **data)
