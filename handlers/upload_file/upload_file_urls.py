#coding:utf-8
from upload_file_handler import (UploadFileHandler, DownloadHandler,
                                 DeleteFileHandler,EidtFilesHandler)

upload_file_url = [
    (r'/uploadfile', UploadFileHandler),
    (r'/downfile', DownloadHandler),
    (r'/deletefile', DeleteFileHandler),
    (r'/editfile', EidtFilesHandler),
]