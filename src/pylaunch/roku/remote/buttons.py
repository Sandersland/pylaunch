from abc import abstractmethod
import tkinter as tk
import threading

MARGIN = 5
BUTTON_HEIGHT = 1
BUTTON_WIDTH = 5
PADDING_X = "2m"
PADDING_Y = "1m"

def threader(func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.start()

class RokuButton(tk.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.configure(
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH
        )
        self.grid(
            sticky="nsew", padx=MARGIN, pady=MARGIN, ipadx=PADDING_X, ipady=PADDING_Y,
        )

    def shape(self, length, width):
        self.grid(rowspan=length, columnspan=width)
        return self

    def place(self, row=0, col=0):
        self.grid(row=row, column=col)
        return self

    @abstractmethod
    def pressed(self, device): pass


class RokuActionButton(RokuButton):
    def __init__(self, root, action, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.action = action

        self.configure(
            height=BUTTON_HEIGHT + 1,
            text=action,
            command=lambda: threader(self.pressed, root.state.selected),
        )
        self.grid(
            sticky="nsew", padx=MARGIN, pady=MARGIN, ipadx=PADDING_X, ipady=PADDING_Y,
        )
        self.shape(1, 2)

    def pressed(self, device):
        if device:
            device.key_press(self.action)
            print(self.action)
        else:
            print("Please select a device.")

class RokuApplicationButton(RokuButton):
    def __init__(self, root, app, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = app

        self.configure(
            height=BUTTON_HEIGHT + 1,
            text=app,
            command=lambda: threader(self.pressed, root.state.selected),
        )
        self.grid(
            sticky="nsew", padx=MARGIN, pady=MARGIN, ipadx=PADDING_X, ipady=PADDING_Y,
        )
        self.shape(1, 6)

    def pressed(self, device):
        if device:
            device[self.app].launch()
            print(self.app)
        else:
            print("Please select a device.")