import functools
import logging
from datetime import timedelta
from io import BytesIO

import minio

from sanaap.exceptions import UploadFailed

logger = logging.getLogger(__name__)


class MinioStorage:
    def __init__(self, client: minio.Minio) -> None:
        self._client = client

    def upload(self, file: BytesIO, bucket: str, name: str, size: int) -> dict:
        """Upload a file to the specified bucket."""
        self._create_bucket(bucket)
        try:
            result = self._client.put_object(
                bucket_name=bucket, object_name=name, data=file, length=size
            )
        except Exception as exc:
            logger.error("failed to upload file to minio", exc_info=True)
            raise UploadFailed("Failed to upload file.") from exc

        return {"bucket": bucket, "name": result.object_name, "etag": result.etag}

    def delete(self, bucket: str, name: str) -> None:
        """Delete an object from the specified bucket."""
        self._client.remove_object(bucket_name=bucket, object_name=name)

    def get_url(self, bucket: str, name: str, ttl: timedelta) -> str:
        """Generate a presigned URL for accessing an object."""
        return self._client.presigned_get_object(
            bucket_name=bucket, object_name=name, expires=ttl
        )

    @functools.cache
    def _create_bucket(self, bucket: str) -> None:
        """Create a new bucket if it does not already exist."""
        if not self._client.bucket_exists(bucket):
            logger.info(f"creating new bucket: {bucket}")
            self._client.make_bucket(bucket)
        else:
            logger.debug(f"bucket {bucket} already exists")
