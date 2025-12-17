import uuid

import pytest

from sanaap.docs.enums import DocStatus
from sanaap.docs.models import Document
from sanaap.exceptions import NotFoundExc
from sanaap.handlers import handle_document_delete
from sanaap.services import MinioStorage

pytestmark = pytest.mark.django_db


def test_handler_deletes_existing_document(storage: MinioStorage, sample_doc: Document):
    handle_document_delete(
        storage=storage, file_uuid=sample_doc.uuid, username="delete-user"
    )
    sample_doc.refresh_from_db()
    assert sample_doc.status == DocStatus.DELETED
    assert "deleted_by" in sample_doc.logs
    assert sample_doc.logs["deleted_by"] == "delete-user"


def test_handle_document_delete_raises_not_found_for_non_existing_uuid(
    storage: MinioStorage,
):
    with pytest.raises(NotFoundExc):
        handle_document_delete(
            storage=storage, file_uuid=uuid.uuid4(), username="delete-user"
        )
