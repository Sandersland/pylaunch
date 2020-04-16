import threading
import tkinter as tk

from pylaunch import roku


MARGIN = 5
BUTTON_WIDTH = 6
BUTTON_PAD_X = "2m"
BUTTON_PAD_Y = "1m"


class Remote:
    def __init__(self, root, model):
        root.bind("<Key>", self.key_press)
        self.model = model

        self.options = {"Select": tuple()}
        self.selected_device = tk.StringVar(root)
        self.selected_device.set("Select")

        self.select_menu = tk.OptionMenu(
            root, self.selected_device, *self.options.keys()
        )
        self.select_menu.pack(expand=True, fill=tk.X)

        self.update_menu()

        self.button_menu = Menu(root, relief="flat", borderwidth=4)
        self.button_menu.pack()

        self.app_menu = AppMenu(root, relief="flat", borderwidth=4)
        self.app_menu.pack(expand=True, fill=tk.X)

    def key_press(self, e):
        char = e.char
        self.model.key_press(e.char)

    def update_menu(self):
        menu = self.select_menu["menu"]

        def update():
            devices = self.model.discover()
            menu.delete(0, "end")
            for d in devices:
                menu.add_command(
                    label=d.friendly_name, command=lambda: self.selected_device.set(d)
                )

        thread = threading.Thread(target=update)
        thread.start()


class Menu(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root

        def new_button(root, text, command, row=0, column=0, margin=MARGIN, sticky=""):
            button = tk.Button(root, command=command)
            button.configure(text=text)
            button.configure(width=BUTTON_WIDTH, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)
            button.grid(row=row, column=column, sticky=sticky, padx=margin, pady=margin)
            return button

        self.home = new_button(
            self, text="Home", command=lambda: self.press_button(roku.HOME)
        )

        self.power = new_button(
            self, text="Power", command=lambda: self.press_button(roku.POWER), column=2
        )

        self.back = new_button(
            self, text="Back", command=lambda: self.press_button(roku.BACK), row=1
        )

        self.up = new_button(
            self, text="Up", command=lambda: self.press_button(roku.UP), row=2, column=1
        )

        self.left = new_button(
            self, text="Left", command=lambda: self.press_button(roku.LEFT), row=3
        )

        self.select = new_button(
            self,
            text="Select",
            command=lambda: self.press_button(roku.SELECT),
            row=3,
            column=1,
        )

        self.right = new_button(
            self,
            text="Right",
            command=lambda: self.press_button(roku.RIGHT),
            row=3,
            column=2,
        )

        self.down = new_button(
            self,
            text="Down",
            command=lambda: self.press_button(roku.DOWN),
            row=4,
            column=1,
        )

    def press_button(self, button):
        print(button)


class AppMenu(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root

        def new_app_button(root, text, command, margin=MARGIN):
            button = tk.Button(root, command=command)
            button.configure(text=text, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)
            button.pack(expand=True, fill=tk.X, padx=margin, pady=margin)
            return button

        self.netflix = new_app_button(
            self, text="Netflix", command=lambda: self.launch_app("Netflix")
        )

    def launch_app(self, app):
        print(app)
