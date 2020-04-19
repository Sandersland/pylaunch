import tkinter as tk

from pylaunch.roku.remote.views import Remote


class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unbind_class("Listbox", "<Key-space>")
        self.resizable(False, False)
        self.title("Roku Remote")
        self.view = Remote(self)

    def run(self):
        self.mainloop()
