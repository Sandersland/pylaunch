import unittest
from unittest.mock import patch, MagicMock

from requests import Response

from pylaunch.dial import Dial


class TestDial(unittest.TestCase):
    @patch("pylaunch.core.requests.get")
    def setUp(self, response):
        with open("tests/xml/dd.xml") as f:
            response.return_value = MagicMock(
                spec=Response,
                text=f.read(),
                headers={"Application-URL": "http://10.1.10.165:8060/dial"},
            )
        self.dial = Dial("https://10.1.10.165:8060/dial/dd.xml")

    def test_address(self):
        self.assertEqual(self.dial.address, "http://10.1.10.165:8060/dial")

    def test_device_type(self):
        self.assertEqual(self.dial.device_type, "urn:roku-com:device:player:1-0")

    def test_friendly_name(self):
        self.assertEqual(self.dial.friendly_name, "NNB CT")

    def test_manufacturer(self):
        self.assertEqual(self.dial.manufacturer, "Roku")

    def test_manufacturer_url(self):
        self.assertEqual(self.dial.manufacturer_url, "http://www.roku.com/")

    def test_model_description(self):
        self.assertEqual(
            self.dial.model_description, "Roku Streaming Player Network Media"
        )

    def test_model_name(self):
        self.assertEqual(self.dial.model_name, "Roku Express")

    def test_model_number(self):
        self.assertEqual(self.dial.model_number, "3900X")

    def test_model_url(self):
        self.assertEqual(self.dial.model_url, "http://www.roku.com/")

    def test_serial_number(self):
        self.assertEqual(self.dial.serial_number, "YG00AE419756")

    def test_udn(self):
        self.assertEqual(self.dial.udn, "uuid:295c0011-5406-1067-80ac-d83134855445")

    def test_launch_app(self):
        pass

    def test_kill_app(self):
        pass

    @patch("requests.get")
    def test_get_app_status(self, response):

        with open("tests/xml/YouTube.xml") as f:
            response.return_value = MagicMock(
                spec=Response, text=f.read(), status_code=200
            )

        app_status = self.dial.get_app_status("YouTube")
        self.assertEquals(
            app_status, {"version": "2.1", "name": "YouTube", "state": "stopped"}
        )
