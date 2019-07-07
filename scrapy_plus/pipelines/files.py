# coding: utf-8
import os
import oss2
from urllib.parse import urlparse

from twisted.internet import threads


class OSSFilesStore(object):
    OSS_ACCESS_KEY = ""
    OSS_ACCESS_SECRET = ""

    def __init__(self, uri):
        #        < Schema >: // < Bucket >.< 外网Endpoint > / < Object >
        u = urlparse(uri)
        self.uri = uri
        self.bucket_name = u.hostname.splite('.')[0]
        self.endpoint = '.'.join(u.hostname.splite('.')[1:])
        self.objectPath = u.path
        self.bucket = oss2.Bucket(oss2.Auth(self.OSS_ACCESS_KEY, self.OSS_ACCESS_SECRET),
                                  self.endpoint, self.bucket_name)

    def stat_file(self, path, info):

        def _onsuccess(meta):
            checksum = meta.headers['ETag']
            last_modified = meta.headers['Last-Modifie']
            return {'checksum': checksum, 'last_modified': last_modified}

        return threads.deferToThread(self.bucket.get_object_meta, path).addCallback(_onsuccess)



    def persist_file(self, path, buf, info, meta=None, headers=None):
        # 首先可以用帮助函数设定分片大小，设我们期望的分片大小为128KB
        total_size = len(buf)
        part_size = oss2.determine_part_size(total_size, preferred_size=128 * 1024)

        # 初始化分片上传，得到Upload ID。接下来的接口都要用到这个Upload ID。
        key = os.path.join(self.objectPath, info)
        upload_id = self.bucket.init_multipart_upload(key).upload_id

        # 逐个上传分片
        # 其中oss2.SizedFileAdapter()把fileobj转换为一个新的文件对象，新的文件对象可读的长度等于size_to_upload
        parts = []
        part_number = 1
        offset = 0
        while offset < total_size:
            size_to_upload = min(part_size, total_size - offset)
            result = self.bucket.upload_part(key, upload_id, part_number,
                                             oss2.SizedFileAdapter(buf, size_to_upload))
            parts.append(oss2.models.PartInfo(part_number,
                                              result.etag,
                                              size=size_to_upload,
                                              part_crc=result.crc))

            offset += size_to_upload
            part_number += 1

            # 完成分片上传
            self.bucket.complete_multipart_upload(key, upload_id, parts)

