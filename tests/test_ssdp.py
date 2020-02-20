from unittest import TestCase
from pylaunch.ssdp import SimpleServiceDiscoveryProtocol, ST_ROKU, DiscoveryMessage


class TestSimpleServiceDiscoveryProtocol(TestCase):
    def setUp(self):
        self.ssdp = SimpleServiceDiscoveryProtocol(ST_ROKU)

    def test_repr(self):
        self.assertEqual(repr(self.ssdp), "SimpleServiceDiscoveryProtocol('roku:ecp')")

    def test_default_timout(self):
        SimpleServiceDiscoveryProtocol.settimeout(1)
        self.assertEqual(self.ssdp.timeout, 1)

    def test_timeout(self):
        SimpleServiceDiscoveryProtocol.settimeout(3)
        ssdp = SimpleServiceDiscoveryProtocol(ST_ROKU)
        self.assertEqual(ssdp.timeout, 3)
        with self.assertRaises(ValueError):
            SimpleServiceDiscoveryProtocol.settimeout("string")

    def test_broadcast(self):
        result = self.ssdp.broadcast()
        self.assertIsInstance(result, list)
        if len(result) > 0:
            (self.assertIsInstance(res, dict) for res in result)
        else:
            print("No response from broadcast.")
            self.assertEqual(result, [])

    def test_message(self):
        search_string = "M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nST:roku:ecp\r\nMX:1\r\nMAN:ssdp:discover\r\n"
        self.assertIsInstance(self.ssdp.message, DiscoveryMessage)
        self.assertEqual(self.ssdp.message, search_string)
