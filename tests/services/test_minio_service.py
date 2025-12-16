import io
from datetime import timedelta
from unittest.mock import Mock, create_autospec

import pytest
from minio import Minio

from sanaap.exceptions import UploadFailed
from sanaap.services import MinioStorage


@pytest.fixture
def mock_client() -> Mock:
    client = create_autospec(Minio)
    return client


@pytest.fixture
def minio_storage(mock_client: Mock) -> MinioStorage:
    return MinioStorage(client=mock_client)


def test_upload_calls_minio_put_object(minio_storage: MinioStorage, mock_client: Mock):
    file_data = io.BytesIO(b"hello world")
    bucket = "test-bucket"
    name = "file.txt"
    size = len(file_data.getbuffer())

    mock_client.bucket_exists.return_value = False
    mock_client.put_object.return_value.object_name = name
    mock_client.put_object.return_value.etag = "etag123"

    result = minio_storage.upload(file=file_data, bucket=bucket, name=name, size=size)

    mock_client.bucket_exists.assert_called_once_with(bucket)
    mock_client.make_bucket.assert_called_once_with(bucket)
    mock_client.put_object.assert_called_once_with(
        bucket_name=bucket, object_name=name, data=file_data, length=size
    )

    assert result == {"bucket": bucket, "name": name, "etag": "etag123"}


def test_upload_raises_on_error(minio_storage: MinioStorage, mock_client: Mock):
    file_data = io.BytesIO(b"hello world")
    bucket = "test-bucket"
    name = "file.txt"
    size = len(file_data.getbuffer())

    mock_client.bucket_exists.return_value = True
    mock_client.put_object.side_effect = Exception("fail")

    with pytest.raises(UploadFailed):
        minio_storage.upload(file=file_data, bucket=bucket, name=name, size=size)


def test_delete_calls_remove_object(minio_storage: MinioStorage, mock_client: Mock):
    bucket = "bucket"
    name = "file.txt"

    minio_storage.delete(bucket=bucket, name=name)
    mock_client.remove_object.assert_called_once_with(
        bucket_name=bucket, object_name=name
    )


def test_get_url_calls_presigned_get_object(
    minio_storage: MinioStorage, mock_client: Mock
):
    bucket = "bucket"
    name = "file.txt"
    ttl = timedelta(seconds=600)
    mock_client.presigned_get_object.return_value = "http://signed-url"

    url = minio_storage.get_url(bucket=bucket, name=name, ttl=ttl)

    mock_client.presigned_get_object.assert_called_once_with(
        bucket_name=bucket, object_name=name, expires=ttl
    )
    assert url == "http://signed-url"


def test_create_bucket_caches(minio_storage: MinioStorage, mock_client: Mock):
    bucket = "bucket"
    mock_client.bucket_exists.side_effect = [False, True]

    minio_storage._create_bucket(bucket)
    minio_storage._create_bucket(bucket)  # second call should use cache

    mock_client.make_bucket.assert_called_once_with(bucket)
