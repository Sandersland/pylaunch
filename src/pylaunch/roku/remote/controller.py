import tkinter as tk

from pylaunch.roku.remote.views import Remote
from pylaunch.roku.remote.models import RokuModel


class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Roku Remote")
        self.model = RokuModel()
        self.view = Remote(self, self.model)

    def run(self):
        self.mainloop()
