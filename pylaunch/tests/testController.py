from pylaunch.dial import Controller, discover
from unittest import TestCase


class testController(TestCase):
    
    def setUp(self):
        self.devices = discover()

    def test_init(self):
        target = self.devices[0]
        self.cont = Controller(target)
        self.assertIsInstance(self.cont, Controller)

    def tearDown(self):
        pass


