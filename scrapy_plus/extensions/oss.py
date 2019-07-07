# -*- coding: utf-8 -*-

from scrapy.extensions.feedexport import BlockingFeedStorage
import oss2
import os
from urllib.parse import urlparse


class OSSFeedStorage(BlockingFeedStorage):
    """
    阿里云OSS存储后端
    """

    def __init__(self, uri):
        #        < Schema >: // < Bucket >.< 外网Endpoint > / < Object >
        u = urlparse(uri)
        self.uri = uri
        self.bucket_name = u.hostname.splite('.')[0]
        self.endpoint = '.'.join(u.hostname.splite('.')[1:])
        self.path = u.path

    def open(self, spider):
        access_key = spider.crawler.settings.get('OSS_ACCESS_KEY')
        access_secret = spider.crawler.settings.get('OSS_ACCESS_SECRET')

        # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
        self.bucket = oss2.Bucket(oss2.Auth(access_key, access_secret),
                                  self.endpoint, self.bucket_name)

    def _store_in_thread(self, file):
        # 首先可以用帮助函数设定分片大小，设我们期望的分片大小为128KB
        total_size = os.path.getsize(file)
        part_size = oss2.determine_part_size(total_size, preferred_size=128 * 1024)

        # 初始化分片上传，得到Upload ID。接下来的接口都要用到这个Upload ID。
        key = file.replace('../', '')
        upload_id = self.bucket.init_multipart_upload(key).upload_id

        # 逐个上传分片
        # 其中oss2.SizedFileAdapter()把fileobj转换为一个新的文件对象，新的文件对象可读的长度等于size_to_upload
        with open(file, 'rb') as fileobj:
            parts = []
            part_number = 1
            offset = 0
            while offset < total_size:
                size_to_upload = min(part_size, total_size - offset)
                result = self.bucket.upload_part(key, upload_id, part_number,
                                                 oss2.SizedFileAdapter(fileobj, size_to_upload))
                parts.append(oss2.models.PartInfo(part_number, result.etag, size=size_to_upload, part_crc=result.crc))

                offset += size_to_upload
                part_number += 1

            # 完成分片上传
            self.bucket.complete_multipart_upload(key, upload_id, parts)

        # 验证一下
        with open(file, 'rb') as fileobj:
            assert self.bucket.get_object(key).read() == fileobj.read()
