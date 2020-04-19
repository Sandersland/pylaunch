import tkinter as tk
from queue import Queue
from threading import Thread
from functools import wraps

from pylaunch import roku
from pylaunch.roku.remote.buttons import RokuActionButton, RokuApplicationButton

SELECT_HEIGHT = 3
SELECT_WIDTH = 30
PADDING_X = "2m"
PADDING_Y = "1m"
SELECT_BG = "black"
SELECT_FG = "green"


def threaded(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        thread = Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    return wrapped


class Remote:
    def __init__(self, root):
        self._keypress_queue = Queue()
        self.state = ApplicationState()
        self.option_select = tk.Listbox(
            root,
            relief=tk.SUNKEN,
            exportselection=False,
            bg=SELECT_BG,
            fg=SELECT_FG,
            selectmode=tk.SINGLE,
            width=SELECT_WIDTH,
            height=SELECT_HEIGHT,
        )
        self.state.set_selector(self.option_select)

        self.option_select.pack(anchor=tk.CENTER)
        self.option_select.bind("<<ListboxSelect>>", self.state.select_device)

        root.bind("<Key>", self.key_press)

        self.state.update_options()

        self.menu = ButtonMenu(root, self.state, relief=tk.FLAT, borderwidth=4)
        self.menu.pack()

    def key_press(self, e=None):
        device = self.state.selected
        self._keypress_queue.put(e.char)
        if device:
            thread = Thread(
                target=device.type_char, args=(self._keypress_queue.get()), daemon=True
            )
            thread.start()
            print(f"pressed {e.char}")
        else:
            print("Please select a device.")


class ApplicationState:
    def __init__(self, selector=None, options=None):
        self.selector = selector
        self.options = options if options else []
        self.selected = None

    def set_selector(self, selector):
        self.selector = selector

    @threaded
    def update_options(self):
        print("discovering devices...")
        self.options = roku.Roku.discover()
        if not len(self.options) > 0:
            self.options = []
        print("Devices discovered!")
        self.selector.delete(0, tk.END)
        for device in self.options:
            self.selector.insert(tk.END, device.friendly_name)
        self.selected = None

    def select_device(self, event=None):
        now = self.selector.curselection()
        if now != self.selected:
            try:
                self.selected = self.options[now[0]]
                print(self.selected)
            except IndexError as e:
                print("We are still looking for devices.")


class ButtonMenu(tk.Frame):
    def __init__(self, root, state, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self._button_pressed_queue = Queue()
        self.state = state

        self.home = RokuActionButton(self, action=roku.HOME)
        self.home.place(2, 0)

        self.power = RokuActionButton(self, action=roku.POWER)
        self.power.place(2, 4)

        self.back = RokuActionButton(self, action=roku.BACK)
        self.back.place(3, 0)

        self.up = RokuActionButton(self, action=roku.UP)
        self.up.place(4, 2)

        self.left = RokuActionButton(self, action=roku.LEFT)
        self.left.place(5, 0)

        self.select = RokuActionButton(self, action=roku.SELECT)
        self.select.place(5, 2)

        self.right = RokuActionButton(self, action=roku.RIGHT)
        self.right.place(5, 4)

        self.down = RokuActionButton(self, action=roku.DOWN)
        self.down.place(6, 2)

        self.netflix = RokuApplicationButton(self, app="Netflix")
        self.netflix.place(7, 0)
