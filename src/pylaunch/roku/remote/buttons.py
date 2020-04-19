from abc import abstractmethod
from threading import Thread
import tkinter as tk

MARGIN = 5
BUTTON_HEIGHT = 1
BUTTON_WIDTH = 5
PADDING_X = "2m"
PADDING_Y = "1m"


class RokuButton(tk.Button):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.configure(height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
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
    def pressed(self, device):
        pass


class RokuActionButton(RokuButton):
    def __init__(self, root, action, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.action = action
        self.configure(
            height=BUTTON_HEIGHT + 1, text=action, command=self.pressed,
        )
        self.grid(
            sticky="nsew", padx=MARGIN, pady=MARGIN, ipadx=PADDING_X, ipady=PADDING_Y,
        )
        self.shape(1, 2)

    def pressed(self):
        device = self.master.state.selected
        self.master._button_pressed_queue.put(self.action)
        if device:
            thread = Thread(
                target=device.key_press,
                args=(self.master._button_pressed_queue.get(),),
                daemon=True,
            )
            thread.start()
            print(f"pressed {self.action}")
        else:
            print("Please select a device.")


class RokuApplicationButton(RokuButton):
    def __init__(self, root, app, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = app

        self.configure(
            height=BUTTON_HEIGHT + 1, text=app, command=self.pressed,
        )
        self.grid(
            sticky="nsew", padx=MARGIN, pady=MARGIN, ipadx=PADDING_X, ipady=PADDING_Y,
        )
        self.shape(1, 6)

    def pressed(self):
        device = self.master.state.selected
        self.master._button_pressed_queue.put(self.app)
        if device:
            thread = Thread(
                target=device[self.master._button_pressed_queue.get()].launch,
                daemon=True,
            )
            thread.start()
            print(f"Pressed {self.app}")
        else:
            print("Please select a device.")
