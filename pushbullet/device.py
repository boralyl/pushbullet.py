from datetime import datetime
import json

import requests


class Device(object):

    PUSH_URL = "https://api.pushbullet.com/v2/pushes"

    def __init__(self, device_id, api_key, access_token, device_info=None):
        self.api_key = api_key
        self.access_token = access_token
        self.auth = access_token if access_token else api_key
        self.device_id = device_id
        device_info = device_info or {}

        self.push_token = device_info.get('push_token')
        self.app_version = device_info.get('app_version')
        self.android_sdk_version = device_info.get('android_sdk_version')
        self.fingerprint = device_info.get('fingerprint')
        self.active = device_info.get('active', False)
        self.nickname = device_info.get('nickname')
        self.manufacturer = device_info.get('manufacturer')
        self.kind = device_info.get('kind')
        self.android_version = device_info.get('android_version')
        self.model = device_info.get('model')
        self.pushable = device_info.get('pushable')

        created = device_info.get('created')
        if created:
            self.created = datetime.fromtimestamp(created)
        else:
            self.created = None
        modified = device_info.get('modified')
        if modified:
            self.modified = datetime.fromtimestamp(modified)
        else:
            self.modified = None

        self._fullname = "{} {} {}".format(self.manufacturer,
                                           self.model, self.android_version)

        self.name = self.nickname or self._fullname

        self._json_header = {'Content-Type': 'application/json'}

    def push_note(self, title, body):
        data = {"type": "note", "title": title, "body": body}
        return self._push(data, headers=self._json_header)

    def push_address(self, name, address):
        data = {"type": "address", "name": name, "address": address}
        return self._push(data, headers=self._json_header)

    def push_list(self, title, items):
        data = {"type": "list", "title": title, "items": items}
        return self._push(data, headers=self._json_header)

    def push_file(self, file):
        raise NotImplemented("v2 file pushing isn't implemented")

    def push_link(self, title, url, body=None):
        data = {"type": "link", "title": title, "url": url, "body": body}
        return self._push(data, headers=self._json_header)

    def _push(self, data, headers={}, files = {}):
        data["device_id"] = self.device_id
        if not files:
            data = json.dumps(data)
        headers.update({"User-Agent": "ifttt2pushbullet.herokuapp.com"})
        return requests.post(self.PUSH_URL, data=data, headers=headers,
                             files=files, auth=(self.auth, ""))

    def __repr__(self):
        return "Device('{}', {})".format(self.api_key, self.device_id)
