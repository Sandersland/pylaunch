import requests
import xmltodict
import re

class DIscoveryAndLaunch:

    def __init__(self, address: str):
        self.bind(address)
        self.active_app = None

    def bind(self, addr):
        resp = requests.get(addr)
        self.address = resp.headers.get('Application-URL')
        xml = xmltodict.parse(resp.text)
        device_info = xml['root']['device']

        for key, value in device_info.items():
            if isinstance(value, str):
                k = '_'.join(re.sub('([a-z])([A-Z])', r'\1 \2', key).split()).lower().replace('-', '_')
                setattr(self, k, value)
    
    def launch_app(self, app_name, **kwargs):
        url = self.address + '/' + app_name
        resp = requests.post(
            url,
            json=kwargs,
            headers={'Content-Type':'application/json'}
        )
        self.active_app = resp.json().get('location')

    def kill_app(self):
        resp = requests.delete(self.active_app)
        if resp.status_code in [200, 204]:
            self.active_app = None
