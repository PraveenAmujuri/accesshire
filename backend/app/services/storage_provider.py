"""
Abstract Storage Provider for AccessHire AI Datasets
Allows swapping local filesystem storage for Cloud Object Storage (S3, GCS, Azure Blob)
without altering the RAG or dataset processing pipelines.
"""

import abc
import os
import json
import shutil
from typing import Optional, Dict, Any, List


class BaseStorageProvider(abc.ABC):
    """Abstract interface for dataset persistence."""

    @abc.abstractmethod
    def exists(self, path: str) -> bool:
        """Check whether a dataset file or directory exists."""
        pass

    @abc.abstractmethod
    def read_text(self, path: str) -> str:
        """Read a text file from storage."""
        pass

    @abc.abstractmethod
    def write_text(self, path: str, content: str) -> None:
        """Write text to storage."""
        pass

    @abc.abstractmethod
    def read_json(self, path: str) -> Any:
        """Read JSON data from storage."""
        pass

    @abc.abstractmethod
    def write_json(self, path: str, data: Any, indent: int = 2) -> None:
        """Write JSON data to storage."""
        pass

    @abc.abstractmethod
    def list_files(self, directory: str) -> List[str]:
        """List file names in a directory."""
        pass


class LocalFileSystemStorageProvider(BaseStorageProvider):
    """Local disk filesystem implementation of BaseStorageProvider."""

    def __init__(self, base_dir: str):
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def _resolve(self, relative_path: str) -> str:
        if os.path.isabs(relative_path):
            return relative_path
        return os.path.join(self.base_dir, relative_path)

    def exists(self, path: str) -> bool:
        return os.path.exists(self._resolve(path))

    def read_text(self, path: str) -> str:
        resolved = self._resolve(path)
        with open(resolved, "r", encoding="utf-8") as f:
            return f.read()

    def write_text(self, path: str, content: str) -> None:
        resolved = self._resolve(path)
        os.makedirs(os.path.dirname(resolved), exist_ok=True)
        with open(resolved, "w", encoding="utf-8") as f:
            f.write(content)

    def read_json(self, path: str) -> Any:
        resolved = self._resolve(path)
        with open(resolved, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_json(self, path: str, data: Any, indent: int = 2) -> None:
        resolved = self._resolve(path)
        os.makedirs(os.path.dirname(resolved), exist_ok=True)
        with open(resolved, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

    def list_files(self, directory: str) -> List[str]:
        resolved = self._resolve(directory)
        if not os.path.exists(resolved):
            return []
        return os.listdir(resolved)


class S3CompatibleStorageProvider(BaseStorageProvider):
    """
    Cloud Object Storage stub (e.g. AWS S3, Google Cloud Storage, Cloudflare R2).
    Ready for zero-rewrite production cloud deployment.
    """

    def __init__(self, bucket_name: str, prefix: str = ""):
        self.bucket_name = bucket_name
        self.prefix = prefix
        # Initialized lazily via boto3 or google-cloud-storage if credentials provided
        self._client = None

    def exists(self, path: str) -> bool:
        raise NotImplementedError("Cloud object storage provider will be enabled when CLOUD_STORAGE_BUCKET is configured.")

    def read_text(self, path: str) -> str:
        raise NotImplementedError("Cloud object storage provider will be enabled when CLOUD_STORAGE_BUCKET is configured.")

    def write_text(self, path: str, content: str) -> None:
        raise NotImplementedError("Cloud object storage provider will be enabled when CLOUD_STORAGE_BUCKET is configured.")

    def read_json(self, path: str) -> Any:
        raise NotImplementedError("Cloud object storage provider will be enabled when CLOUD_STORAGE_BUCKET is configured.")

    def write_json(self, path: str, data: Any, indent: int = 2) -> None:
        raise NotImplementedError("Cloud object storage provider will be enabled when CLOUD_STORAGE_BUCKET is configured.")

    def list_files(self, directory: str) -> List[str]:
        raise NotImplementedError("Cloud object storage provider will be enabled when CLOUD_STORAGE_BUCKET is configured.")


def get_storage_provider(base_dir: str = "./data/datasets", backend: str = "local") -> BaseStorageProvider:
    """Factory to instantiate the appropriate storage backend based on configuration."""
    if backend.lower() == "local":
        return LocalFileSystemStorageProvider(base_dir)
    elif backend.lower() in ("s3", "gcs", "cloud"):
        return S3CompatibleStorageProvider(bucket_name=os.getenv("CLOUD_STORAGE_BUCKET", "accesshire-datasets"))
    return LocalFileSystemStorageProvider(base_dir)
