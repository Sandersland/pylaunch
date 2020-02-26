import unittest
from pylaunch.ssdp import SimpleServiceDiscoveryProtocol, ST_ROKU, DiscoveryMessage


class TestSimpleServiceDiscoveryProtocol(unittest.TestCase):
    def setUp(self):
        self.ssdp = SimpleServiceDiscoveryProtocol(ST_ROKU)

    def test_repr(self):
        self.assertEqual(repr(self.ssdp), "SimpleServiceDiscoveryProtocol('roku:ecp')")

    def test_default_timout(self):
        self.assertEqual(self.ssdp.timeout, 1)

    def test_timeout(self):
        ssdp = SimpleServiceDiscoveryProtocol(ST_ROKU)
        ssdp.settimeout(3)
        self.assertEqual(ssdp.timeout, 3)
        with self.assertRaises(ValueError):
            ssdp.settimeout("string")

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
