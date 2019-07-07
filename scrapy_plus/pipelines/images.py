# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline as _ImagesPipeline
from scrapy.pipelines.files import FSFilesStore, S3FilesStore, GCSFilesStore
from .files import OSSFilesStore

class ImagesPipeline(_ImagesPipeline):
    STORE_SCHEMES = {
        '': FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'oss':OSSFilesStore
    }

    def __init__(self, store_uri, download_func=None, settings=None):
        super(ImagesPipeline, self).__init__(store_uri, settings=settings,
                                             download_func=download_func)

    @classmethod
    def from_settings(cls, settings):
        s3store = cls.STORE_SCHEMES['s3']
        s3store.AWS_ACCESS_KEY_ID = settings['AWS_ACCESS_KEY_ID']
        s3store.AWS_SECRET_ACCESS_KEY = settings['AWS_SECRET_ACCESS_KEY']
        s3store.POLICY = settings['IMAGES_STORE_S3_ACL']

        gcs_store = cls.STORE_SCHEMES['gs']
        gcs_store.GCS_PROJECT_ID = settings['GCS_PROJECT_ID']
        gcs_store.POLICY = settings['IMAGES_STORE_GCS_ACL'] or None

        ossStore = cls.STORE_SCHEMES['oss']
        ossStore.OSS_ACCESS_KEY = settings['OSS_ACCESS_KEY']
        ossStore.OSS_ACCESS_SECRET = settings['OSS_ACCESS_SECRET']

        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)