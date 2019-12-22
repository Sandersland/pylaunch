import requests
import xmltodict
import re
from urllib.parse import unquote

class DIscoveryAndLaunch:

    def __init__(self, address: str):
        self.bind(address)
        self.instance_url = None
        self.refresh_url = None

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
        self.refresh_url = unquote(resp.text)
        self.instance_url = resp.headers.get('location')

    def kill_app(self):
        '''
        This will kill any active application tracked by this instance if one exists and will return True if successful otherwise it will return False.
        '''
        if not self.instance_url:
            raise Exception("There is no instance found to kill.")
        resp = requests.delete(self.instance_url)
        if resp.status_code in [200, 204]:
            self.instance_url = None
            self.refresh_url = None
            return True
        else:
            return False

    def refresh_instance(self, inplace=False):
        resp = requests.post(self.refresh_url)
        instance_url = resp.headers.get('location')
        if inplace:
            self.instance_url = instance_url
        else:
            return instance_url

    