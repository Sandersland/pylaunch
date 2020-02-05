from unittest import TestCase
from src.pylaunch.ssdp import SimpleServiceDiscoveryProtocol, ST_ROKU, DiscoveryMessage


class TestSimpleServiceDiscoveryProtocol(TestCase):
    def setUp(self):
        self.ssdp = SimpleServiceDiscoveryProtocol(ST_ROKU)

    def tearDown(self):
        pass

    def test_default_timout(self):
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

    def test_message(self):
        self.assertIsInstance(self.ssdp.message, DiscoveryMessage)
