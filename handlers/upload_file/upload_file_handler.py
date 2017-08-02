#coding:utf-8
from handlers.base.base_handler import BaseHandler
from models.upload_file.upload_file_model import Files
from handlers.admin.admin_handler import HasPermission


class UploadFileHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('admin/upload_file.html', msg='')

    def post(self):
        filename_post = self.request.files.get('myfilename', '')
        print filename_post
        for files in filename_post:
            msg = self.save_file(files)
            self.render('admin/upload_file.html', msg=msg)

    def save_file(self, files):
        file_name = files['filename']
        url = 'files/upload_files/' + file_name
        if Files.file_is_existed(files['body']):
            return '文件已经存在'
        with open(url, 'wb') as f:
            f.write(files['body'])
        fi = Files()
        fi.filename = file_name
        fi.content_length = len(files['body'])
        fi.content_type = files['content_type']
        fi.file_hash = files['body']
        # fi.upload_user = self.current_user.username
        self.db.add(fi)
        self.db.commit()
        return '文件保存成功'


class DownloadHandler(BaseHandler):
    def get(self):
        filename = self.get_argument('filename', '')
        print filename
        if len(filename)>0:
            filepath = 'files/upload_files/' + filename
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + filename)
            with open(filepath, 'rb') as f:
                while 1:
                    data = f.read(2048)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        else:
            self.write('no filename')


def has_permission_delete_files(self, filename, types):
    if HasPermission().has_permission(self, filename, types):
        return True
    return False


class  DeleteFileHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        files = self.db.query(Files).filter(Files.uuid == uuid).first()
        if uuid:
            if files.p_id:
                if not has_permission_delete_files(self, files.filename, "files"):
                    return self.write('没权限')
            files.locked = True
            self.db.add(files)
            self.db.commit()
            self.redirect('/filestable/1')
        else:
            self.write('no file uuid')


class EidtFilesHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        if uuid:
            files = Files.by_uuid(uuid)
            self.render('admin/edit_file.html', files=files)

    def post(self):
        name = self.get_argument('name', '')
        uuid = self.get_argument('uuid', '')
        if name:
            try:
                files = Files.by_uuid(uuid)
                files.p_id = int(name)
                self.db.add(files)
                self.db.commit()
                self.redirect('/filestable/1')
            except Exception as e:
                self.write('没此权限')
        else:
            self.write('no name')


