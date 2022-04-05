#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging

import yaml
import requests

from xenoslib.base import SingletonWithArgs


logger = logging.getLogger(__name__)


class YamlConfig(SingletonWithArgs, dict):
    """config in yaml, can work as a dict"""

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, name, value):
        try:
            getattr(super(), name)
        except AttributeError as exc:
            if str(exc).startswith("'super' object has no attribute "):
                self[name] = value
                return
            raise exc
        raise AttributeError(f"'{__class__.__name__}' object attribute '{name}' is read-only")

    def __str__(self):
        return yaml.safe_dump(self.copy(), allow_unicode=True)

    def __init__(self, config_file='config.yml'):
        if self._config_file:
            return
        super().__setattr__('_config_file', config_file)
        if os.path.exists(config_file):
            with open(config_file, encoding='utf-8') as r:
                self.update(yaml.safe_load(r))

    def save(self):
        data = str(self)
        with open(self._config_file, 'w', encoding='utf-8') as w:
            w.write(data)
            # yaml.safe_dump(self.copy(), w, allow_unicode=True)


class RequestAdapter:
    def request(self, method, path, *args, **kwargs):
        url = f'{self.base_url}/{path}'
        logger.debug(url)
        response = self.session.request(method, url, *args, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except Exception as exc:
            logger.debug(exc)
            logger.debug(response)
            return response.text

    def get(self, path, *args, **kwargs):
        return self.request('get', path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request('post', path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.request('put', path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request('delete', path, *args, **kwargs)

    def __init__(self):
        self.session = requests.Session()


class OneDrive(RequestAdapter):
    """
    onedrive for business with certain accounts
    https://docs.microsoft.com/zh-cn/onedrive/developer/rest-api/?view=odsp-graph-online
    """

    base_url = 'https://graph.microsoft.com/v1.0'
    auth_url_template = 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'

    # https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
    tenant = '0dc0acdd-87c8-4aa5-b794-f7918e012b77'
    client_id = '5195c197-4ad7-47e1-abf6-1e86d53f9dec'
    client_secret = 'b467Q~Zi1Svi0s2aksB2HHK-Uk~YAHjCTumXx'

    def __init__(self, username=None, password=None):
        self.session = requests.Session()
        if username and password:
            self.auth(username, password)

    def auth(self, username, password):
        """https://docs.microsoft.com/zh-cn/azure/active-directory/develop/v2-oauth-ropc"""
        auth_url = self.auth_url_template.format(tenant=self.tenant)
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': username,
            'password': password,
            'scope': 'user.read openid profile offline_access',
            'grant_type': 'password',
        }
        response = self.session.post(auth_url, data=data)
        response.raise_for_status()
        self.session.headers.update(
            {
                'Authorization': f'Bearer {response.json()["access_token"]}',
                'Accept': 'application/json',
            }
        )

    def drives(self):
        return self.get('/me/drives/')

    def children(self):
        return self.get('/me/drive/root/children')

    def mkdir(self):
        data = {"name": "New Folder", "folder": {}, "@microsoft.graph.conflictBehavior": "rename"}
        return self.post('/me/drive/root/children', json=data)

    def upload_file(self, filepath, folder='/'):
        """
        https://docs.microsoft.com/zh-cn/onedrive/developer/rest-api/api/driveitem_put_content?view=odsp-graph-online
        upload file with size uplimit to 4M, to upload bigger file use upload_bigfile()
        """
        with open(filepath, 'rb') as r:
            data = r.read()
            return self.put(f'/me/drive/root:/{folder}/{filepath}:/content', data=data)

    def create_upload_session(self, filepath, folder='/'):
        """
        https://docs.microsoft.com/zh-cn/onedrive/developer/rest-api/api/driveitem_createuploadsession?view=odsp-graph-online
        """
        data = {  # noqa
            "@microsoft.graph.conflictBehavior": "rename | fail | replace",
            "description": "description",
            "fileSystemInfo": {"@odata.type": "microsoft.graph.fileSystemInfo"},
            "name": "filename.txt",
        }  # optional, not used
        res = self.post(f'/me/drive/root:{folder}/{filepath}:/createUploadSession')
        return res.get('uploadUrl')

    def upload(self, filepath, folder='/'):
        total_chunk = os.path.getsize(filepath)
        if total_chunk < 4 * 1024 * 1024:
            return self.upload_file(filepath, folder)
        return self.upload_bigfile(filepath, total_chunk, folder)

    def upload_bigfile(self, filepath, total_chunk, folder='/', chunk_size=60 * 1024 * 1024):
        url = self.create_upload_session(filepath, folder)
        with open(filepath, 'rb') as r:
            current_chunk = 0
            while current_chunk < total_chunk:
                data = r.read(chunk_size)
                chunk_end = min(current_chunk + chunk_size - 1, total_chunk - 1)
                headers = {
                    'Content-Range': f'bytes {current_chunk}-{chunk_end}/{total_chunk}'
                }  # 'Content-Range': 'bytes 0-25/128'
                logger.debug(f"Content-Range: {headers['Content-Range']}")
                res = self.session.put(url=url, headers=headers, data=data)
                current_chunk += chunk_size
            return res.json()


def del_to_recyclebin(filepath, on_fail_delete=False):
    """delete file to recyclebin if possible"""
    if not sys.platform == 'win32':
        if on_fail_delete:
            os.remove(filepath)
            return True
        return False
    from win32com.shell import shell, shellcon

    res, _ = shell.SHFileOperation(
        (
            0,
            shellcon.FO_DELETE,
            filepath,
            None,
            shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
            None,
            None,
        )
    )
    return res == 0


def send_notify(msg, key):
    """send a message for ifttt"""
    url = f'https://maker.ifttt.com/trigger/message/with/key/{key}'
    data = {'value1': msg}
    return requests.post(url, data=data)


class IFTTTLogHandler(logging.Handler):
    """
    log handler for IFTTT
    usage：
    key = 'xxxxx.xxxzx.xxxzx.xxxzx'
    iftttloghandler = IFTTTLogHandler(key, level=logging.INFO)
    logging.getLogger(__name__).addHandler(iftttloghandler)
    """

    def __init__(self, key, level=logging.CRITICAL, *args, **kwargs):
        self.key = key
        super().__init__(level=level, *args, **kwargs)

    def emit(self, record):
        try:
            send_notify(self.format(record), self.key)
        except Exception as exc:
            logging.getlog(__name__).warning(exc, exc_info=True)


if __name__ == '__main__':
    # import glob
    # for path in glob.iglob('*.yml'):
    # config = YamlConfig(path)
    # print(config)
    # config.save()
    config = YamlConfig()
    config.on = 'test'
    print(config)
