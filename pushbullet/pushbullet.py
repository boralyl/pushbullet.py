from itertools import chain

import requests
import sys
from .device import Device

if sys.version_info >= (3, 0, 0):
    integer_type = (int,)
else:
    integer_type = (int, long)


class PushBullet(object):

    DEVICES_LIST_URL = "https://api.pushbullet.com/v2/devices"

    def __init__(self, api_key=None, access_token=None):
        self.api_key = api_key
        self.access_token = access_token
        if not self.api_key and not self.access_token:
            raise Exception("api_key or access_token params required")
        self.auth = access_token if access_token else api_key

        self._devices = []
        self._load_devices()

    def _load_devices(self):
        resp = requests.get(self.DEVICES_LIST_URL, auth=(self.auth, ""))
        resp_dict = resp.json()

        own_devices = resp_dict.get("devices", [])
        shared_devices = resp_dict.get("shared_devices", [])

        devices = []
        for device_info in chain(own_devices, shared_devices):
            d = Device(device_info["iden"], self.api_key, self.access_token,
                       device_info)
            devices.append(d)

        self._devices = devices

    def reload_devices(self):
        self._load_devices()

    @property
    def devices(self):
        return self._devices

    def get(self, query):
        device = list(filter(lambda x: x.device_id == query, self._devices))
        if not device:
            return None
        else:
            return device[0]

    def __getitem__(self, device_id):
        return self.get(device_id)
