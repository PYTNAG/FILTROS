from tkinter import *
from HexColor import *


class App:
    __rows = 1
    __cols = 1
    __widgets = {}
    __version = 'a 1.0'

    def __init__(self, title: str):
        self.__root = Tk()
        self.__root.title(f"{title} [{self.__version}]")

    def get_widget(self, name: str):
        return self.__widgets[name][0]

    def add_widget(self,
                   name: str,
                   widget: Widget,
                   row: int,
                   col: int,
                   col_span: int = 1) -> None:
        self.__widgets[name] = (widget, row, col, col_span)

    def get_label(self, text: str) -> Label:
        return Label(
            self.__root,
            text=text
        )

    def get_button(self, text: str, size: tuple) -> Button:
        return Button(
            self.__root,
            text=text,
            width=size[0],
            height=size[1]
        )

    def set_button_command(self,
                           btn_name: str,
                           command: callable):
        if btn_name in self.__widgets:
            self.__widgets[btn_name][0].config(command=command)
        else:
            raise ValueError('Unknown button')

    def get_entry(self, width: int = 100) -> Entry:
        return Entry(
            self.__root,
            width=width
        )

    def get_canvas(self, width: int = 500, height: int = 500, bg_color: HexRGB = HexRGB(255, 255, 255)) -> Canvas:
        return Canvas(
            self.__root,
            width=width,
            height=height,
            bg=bg_color.get_hex()
        )

    def grid_widgets(self):
        for widget in self.__widgets.values():
            widget[0].grid(row=widget[1], column=widget[2], columnspan=widget[3])

    def start(self):
        self.grid_widgets()
        self.__root.mainloop()
