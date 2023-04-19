from tkinter import *


class App:
    __widgets = {}

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__root = Tk()

    def add_row(self, name: str, widget: Widget) -> None:
        self.__widgets[name] = widget

    def get_label(self, text: str) -> Label:
        return Label(
            self.__root,
            text=text
        )

    def get_button(self,
                   text: str = 'button',
                   size: tuple = (30, 5),
                   func: callable = lambda: 0) -> Button:
        return Button(
            self.__root,
            text=text,
            width=size[0],
            height=size[1],
            command=func
        )

    def get_entry(self, width: int = 100):
        return Entry(
            self.__root,
            width
        )

    def get_canvas(self,
                   width: int = 500,
                   height: int = 500,
                   bg: str = 'white') -> Canvas:
        return Canvas(
            self.__root,
            width=width,
            height=height,
            bg=bg
        )

    def start(self):
        self.__root.mainloop()
