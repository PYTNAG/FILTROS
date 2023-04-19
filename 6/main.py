from tkinter import *
from PIL import Image, ImageDraw
import math
import os
import random


class R2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_color(self) -> list:
        x = self.x
        y = self.y

        delta = [
            abs(eval(x_entry.get()) - x),
            abs(eval(y_entry.get()) - y)
        ]

        dr = (delta[0] ** 2 + delta[1] ** 2) ** 0.5

        r = 0 if delta[0] == 0 else (255 * (1 - x / delta[0])) % 256
        b = 0 if delta[1] == 0 else (255 * (1 - y / delta[1])) % 256

        g = (math.cos(2 * math.pi / 10 * dr) + 1) * 255 / 2

        return [round(r), round(g), round(b)]


def get_hex_by_byte(byte):
    _hex = hex(byte)[2:]
    if len(_hex) == 1:
        return '0' + _hex
    elif _hex == "100":
        return 'FF'
    return _hex


def get_hex(rgb: list):
    r = get_hex_by_byte(rgb[0])
    g = get_hex_by_byte(rgb[1])
    b = get_hex_by_byte(rgb[2])
    return f"#{r}{g}{b}"


def get_pixel_by_position(x: int, y: int) -> list:
    # n = int(eval(num_entry.get()) % len(files))
    # _r, _g, _b = bank[int(n % len(files))].getpixel((x, y))
    # return [_r, _g, _b]
    return R2(x, y).get_color()


def generate():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            pixel = get_pixel_by_position(x, y)
            canv.create_rectangle(x, y, x, y, outline=get_hex(pixel))
            image_to_save.putpixel((x, y), tuple(pixel))


def save():
    file = open('eq.txt', 'a')
    file.write(f"x: {x_entry.get()}\n")
    file.write(f"y: {y_entry.get()}\n")
    # file.write(f"z: {z_entry.get()}\n")
    file.write(f"file: {ent.get()}\n")
    file.write("\n")
    file.close()
    image_to_save.save(ent.get() + '.png')


WIDTH = 500
HEIGHT = 500

image_to_save = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))

root = Tk()

canv = Canvas(root,
              width=WIDTH,
              height=HEIGHT,
              bg='white')
canv.grid(row=1, column=1, columnspan=2)

# X
x_label = Label(root,
                  text="f(x) = : ")
x_label.grid(row=2, column=1)

x_entry = Entry(root, width=100)
x_entry.grid(row=2, column=2)

# Y
y_label = Label(root,
                  text="f(y) = : ")
y_label.grid(row=3, column=1)

y_entry = Entry(root, width=100)
y_entry.grid(row=3, column=2)

# Z
# z_label = Label(root,
#                   text="f(z) = : ")
# z_label.grid(row=2, column=1)
#
# z_entry = Entry(root, width=100)
# z_entry.grid(row=2, column=2)

btn = Button(root,
             text='Generate',
             width=30,
             height=5,
             bg='white',
             fg='black')
btn.config(command=generate)
btn.grid(row=4, column=1, columnspan=2)

# save
ent = Entry(root,
            width=30)
ent.grid(row=5, column=1, columnspan=2)

btn = Button(root,
             text='Save',
             width=30,
             height=5,
             bg='white',
             fg='black')
btn.config(command=save)
btn.grid(row=6, column=1, columnspan=2)
root.mainloop()
