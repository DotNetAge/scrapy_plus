# -*- coding: utf-8 -*-

from scrapy.extensions.feedexport import BlockingFeedStorage
from scrapy.exceptions import NotConfigured
import oss2
from urllib.parse import urlparse


class OSSFeedStorage(BlockingFeedStorage):
    """
    阿里云OSS存储后端
    """

    def __init__(self, uri):
        from scrapy.conf import settings
        try:
            import oss2
        except ImportError:
            raise NotConfigured()

        # self.connect_s3 = boto.connect_s3

        u = urlparse(uri)
        self.uri = uri
        self.bucketname = u.hostname
        self.access_key = u.username or settings['OSS_ACCESS_KEY_ID']
        self.secret_key = u.password or settings['OSS_SECRET_ACCESS_KEY']
        self.keyname = u.path

    def _store_in_thread(self, file):
        file.seek(0)
        auth = oss2.Auth(self.access_key, self.secret_key)
        # bucket = oss2.Bucket(auth,'http://oss-cn-hangzhou.aliyuncs.com','bucket名称') 阿里云的用法参考
        bucket = oss2.Bucket(auth, self.uri,
                             self.bucketname)  # 有问题
        bucket.put_object_from_file(file.name, file.name)

        # conn = self.connect_s3(self.access_key, self.secret_key)
        #bucket = conn.get_bucket(self.bucketname, validate=False)
        #key = bucket.new_key(self.keyname)
        # key.set_contents_from_file(file)
        # key.close()
