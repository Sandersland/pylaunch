import unittest
from unittest.mock import patch, MagicMock

from requests import Response

from pylaunch.roku import Roku
from pylaunch.ssdp import HTTPResponse


class TestRoku(unittest.TestCase):
    @patch("pylaunch.core.requests.get")
    def setUp(self, response):
        with open("tests/xml/example.xml") as f:
            response.return_value = MagicMock(spec=Response, headers={}, text=f.read())
        self.roku = Roku("https://10.1.10.165:8060")

    def test_address(self):
        self.assertEqual(self.roku.address, "http://10.1.10.165:8060")

    def test_device_type(self):
        self.assertEqual(self.roku.device_type, "urn:roku-com:device:player:1-0")

    def test_friendly_name(self):
        self.assertEqual(self.roku.friendly_name, "Whcowork TV")

    def test_manufacturer(self):
        self.assertEqual(self.roku.manufacturer, "Roku")

    def test_manufacturer_url(self):
        self.assertEqual(self.roku.manufacturer_url, "http://www.roku.com/")

    def test_model_description(self):
        self.assertEqual(
            self.roku.model_description, "Roku Streaming Player Network Media"
        )

    def test_model_name(self):
        self.assertEqual(self.roku.model_name, "LC-55LBU591U")

    def test_model_number(self):
        self.assertEqual(self.roku.model_number, "7000X")

    def test_model_url(self):
        self.assertEqual(self.roku.model_url, "http://www.roku.com/")

    def test_serial_number(self):
        self.assertEqual(self.roku.serial_number, "YN00RW847759")

    def test_udn(self):
        self.assertEqual(self.roku.udn, "uuid:29780022-9c0c-10ef-808f-00f48d382d34")

    @patch("pylaunch.core.requests.get")
    def test_info(self, response):

        with open("tests/xml/device-info.xml") as f:
            response.return_value.text = f.read()

        roku_info = self.roku.info
        self.assertIsInstance(roku_info, dict)
        self.assertTrue("power_mode" in roku_info)
        self.assertFalse("asdvd137sdf" in roku_info)

    @patch("pylaunch.core.requests.get")
    def test_apps(self, response):

        with open("tests/xml/apps.xml") as f:
            response.return_value.text = f.read()

        apps = self.roku.apps
        self.assertIsInstance(apps, dict)
        self.assertTrue("Netflix" in apps)
        self.assertFalse("asdasdasd" in apps)

    @patch("pylaunch.core.requests.get")
    def test_active_app(self, response):
        with open("tests/xml/active-app.xml") as f:
            response.return_value.text = f.read()
        app = self.roku.active_app
        self.assertTrue(app.name == "Roku")

    @patch("src.pylaunch.ssdp.SimpleServiceDiscoveryProtocol.broadcast")
    def test_discover(self, response):
        message = MagicMock(
            spec=HTTPResponse, headers={"location": "http://192.168.1.1"}
        )
        response.return_value = [message]
        devices = Roku.discover()
        self.assertIsInstance(devices, list)
        [self.assertIsInstance(x, Roku) for x in devices]
