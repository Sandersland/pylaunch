import unittest
from unittest.mock import patch, Mock

from pylaunch.roku import Roku


class TestRoku(unittest.TestCase):
    def setUp(self):
        self.roku = Roku("https://10.1.10.165:8060/")

    def test_address(self):
        self.assertEqual(self.roku.address, "http://10.1.10.165:8060")

    @patch("requests.get")
    def test_info(self, mock_get):

        with open("tests/device-info.xml") as f:
            mock_get.return_value.text = f.read()

        roku_info = self.roku.info
        self.assertIsInstance(roku_info, dict)
        self.assertTrue("power_mode" in roku_info)
        self.assertFalse("asdvd137sdf" in roku_info)

    @patch("requests.get")
    def test_apps(self, mock_get):
        with open("tests/apps.xml") as f:
            mock_get.return_value.text = f.read()
        apps = self.roku.apps
        self.assertIsInstance(apps, dict)
        self.assertTrue("Netflix" in apps)
        self.assertFalse("asdasdasd" in apps)

    @patch("requests.get")
    def test_active_app(self, mock_get):
        with open("tests/active-app.xml") as f:
            mock_get.return_value.text = f.read()
        app = self.roku.active_app
        self.assertTrue(app.name == "Roku")

    @patch("pylaunch.roku.main.SimpleServiceDiscoveryProtocol.broadcast")
    def test_discover(self, mock_scan):
        message = Mock(headers={"location": "http://192.168.1.1"})
        mock_scan.return_value = [message]
        devices = Roku.discover()
        self.assertIsInstance(devices, list)
        [self.assertIsInstance(x, Roku) for x in devices]
