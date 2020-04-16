from threading import Thread

from pylaunch import roku


class RokuModel:
    def __init__(self):
        devices = []
        selected_device = None

    def choose_device(self, idx):
        self.selected_device = self.device[idx]

    @staticmethod
    def discover():
        return roku.Roku.discover()

    @staticmethod
    def key_press(device, key):
        device.key_press(key)
