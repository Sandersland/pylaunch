import requests
import xmltodict
import re
from urllib.parse import unquote, urlencode

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
    
    def launch_app(self, app_name, callback=None, **kwargs):
        url = self.address + '/' + app_name
        resp = requests.post(
            url,
            data=urlencode(kwargs).encode('utf8'),
            headers={'Content-Type':'application/json'}
        )
        print(resp.url)
        print(resp.status_code)
        self.refresh_url = unquote(resp.text)
        self.instance_url = resp.headers.get('location')
        callback(resp) if callback else None

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

if __name__ == '__main__':
    from time import sleep
    from ssdp import SimpleServiceDiscoveryProtocol, ST_DIAL
    SimpleServiceDiscoveryProtocol.settimeout(3)
    devices = SimpleServiceDiscoveryProtocol(ST_DIAL).broadcast()
    loc = devices[0].headers.get('location')
    d = DIscoveryAndLaunch(loc)
    d.launch_app('YouTube', v="uigUeW05HSM")
    print(d.instance_url)
    print(d.refresh_url)
    # requests.post("http://192.168.0.7:8060/dial_extra_data/YouTube", json={"v": "uigUeW05HSM"})

    
    

    
