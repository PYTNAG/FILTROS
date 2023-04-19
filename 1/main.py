from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import math
import os


def GetHexByByte(byte):
    _hex = hex(byte)[2:]
    if len(_hex) == 1:
        return '0' + _hex
    elif _hex == "100":
        return 'FF'
    return _hex


def GetHex(rgb):
    r = GetHexByByte(rgb[0])
    g = GetHexByByte(rgb[1])
    b = GetHexByByte(rgb[2])
    return f"#{r}{g}{b}"


def GetColorByPos(x, y):
    _r = int(eval(red_ent.get()) % 256)
    _g = int(eval(green_ent.get()) % 256)
    _b = int(eval(blue_ent.get()) % 256)
    _a = int(eval(alpha_ent.get()) % 256)
    return [_r, _g, _b, _a]


def Draw():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            rgba = GetColorByPos(x, y)
            rgb = (rgba[0], rgba[1], rgba[2], 255)
            canv.create_rectangle(x, y, x, y, outline=GetHex(rgb))
            img.putpixel((x, y), rgb)
    #img.save('tmp.png')
    #canv.create_image(500, 500, image=PhotoImage('tmp.png'))
    #os.remove('tmp.png')


def Save():
    file = open('eq.txt', 'a')
    file.write(f"r: {red_ent.get()}\n")
    file.write(f"g: {green_ent.get()}\n")
    file.write(f"b: {blue_ent.get()}\n")
    file.write(f"a: {alpha_ent.get()}\n")
    file.write(f"file: {ent.get()}\n")
    file.write("\n")
    file.close()
    img.save(ent.get() + '.png')


WIDTH = 500
HEIGHT = 500

img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 1))

root = Tk()

canv = Canvas(root,
              width=WIDTH,
              height=HEIGHT,
              bg='white')
canv.grid(row=1, column=1, columnspan=2)

red_label = Label(root,
                  text="RED: ")
red_label.grid(row=2, column=1)
red_ent = Entry(root, width=100)
red_ent.grid(row=2, column=2)

green_label = Label(root,
                  text="GREEN: ")
green_label.grid(row=3, column=1)
green_ent = Entry(root, width=100)
green_ent.grid(row=3, column=2)

blue_label = Label(root,
                  text="BLUE: ")
blue_label.grid(row=4, column=1)
blue_ent = Entry(root, width=100)
blue_ent.grid(row=4, column=2)

alpha_label = Label(root,
                  text="ALPHA: ")
alpha_label.grid(row=5, column=1)
alpha_ent = Entry(root, width=100)
alpha_ent.grid(row=5, column=2)

btn = Button(root,
             text='Draw',
             width=30,
             height=5,
             bg='white',
             fg='black')
btn.config(command=Draw)
btn.grid(row=6, column=1, columnspan=2)

ent = Entry(root,
            width=30)
ent.grid(row=7, column=1, columnspan=2)

btn = Button(root,
             text='Save',
             width=30,
             height=5,
             bg='white',
             fg='black')
btn.config(command=Save)
btn.grid(row=8, column=1, columnspan=2)
root.mainloop()
