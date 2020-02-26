from pylaunch.xmlparse import XMLFile, normalize
import unittest


class test_XMLFile(unittest.TestCase):
    def setUp(self):
        with open("tests/xml/example.xml", "r") as file:
            filestring = file.read()
            self.xml = XMLFile(filestring)

    def test_namespace(self):
        self.assertTrue(self.xml.namespace == "{urn:schemas-upnp-org:device-1-0}")

    def test_find(self):
        friendly_name = self.xml.find("friendlyName")
        self.assertTrue(friendly_name.text == "Whcowork TV")
        url = self.xml.find("url")
        self.assertTrue(url.text == "device-image.png")

    def test_normalize(self):
        model_name = self.xml.find("modelName")
        self.assertTrue(
            normalize(self.xml, model_name) == ("model_name", "LC-55LBU591U")
        )

        manufacturer_url = self.xml.find("manufacturerURL")
        self.assertTrue(
            normalize(self.xml, manufacturer_url)
            == ("manufacturer_url", "http://www.roku.com/")
        )

        spec_version = self.xml.find("specVersion")
        self.assertTrue(normalize(self.xml, spec_version) == ("spec_version", None))
