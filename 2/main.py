from tkinter import *
from PIL import Image, ImageDraw
import math
import os
import random

from numpy import arange


def GetHexByByte(byte):
    _hex = hex(byte)[2:]
    if len(_hex) == 1:
        return '0' + _hex
    elif _hex == "100":
        return 'FF'
    return _hex


def GetHex(rgb: list):
    r = GetHexByByte(rgb[0])
    g = GetHexByByte(rgb[1])
    b = GetHexByByte(rgb[2])
    return f"#{r}{g}{b}"


def GetImage(n: int):
    return bank[n % len(files)]


def GetPixelByPos(x: int, y: int, q = 1) -> list[int]:
    # <!-- to delete
    #d20_1 = (((x - 240)/20.0)**20 + ((y - 581)/20.0)**20)**(1/20.0)
    #d20_2 = (((x - 718)/20.0)**20 + ((y - 386)/20.0)**20)**(1/20.0)

    d = lambda x,y,n=2: ((x/5.0)**n + (y/5.0)**n)**(1/float(n))
    # -->
    #n = int(eval(num_entry.get()) % len(files))
    #n = int(((d20_1 * d20_2) / eval(num_entry.get())) % len(files))
    # try:
    #     n = d(d(abs(x-519),abs(y-581),5), d(abs(x-439),abs(y-386),5), 4) % len(files)
    # except:
    #     n = 0
    #  _r, _g, _b = bank[int(n % len(files))].getpixel((x, y))
    # return [_r, _g, _b]

    center = [500, 500]

    # f = lambda d: round((len(files) - 1) / 2.0 * (math.sin(math.pi / 200.0 * d) + 1))

    b = float(len(files))

    k = - math.log(1.0/(2*b - 1)) / 250.0

    s = lambda x: math.sin(math.pi / 51.0 * x)
    f = lambda x, y: round(255 / 2.0 * (s(d(x - center[0], y - center[1])) + 1))

    s_r = f(x, 0)
    s_g = f(0, y)
    s_b = f(x, y)

    _main = int(round(d(x - center[0], y - center[1])) % b)

    

    flt = lambda x, t: x > t
    norm = lambda x, k = 1, t = 200: x if not flt(x, t) else (255 - x * k if 255 > x * k else (x * k - 255) % 256)

    # red
    o_r = tuple(bank[_main].getpixel((x, y)))[0]
    dr = 255 - o_r
    # _r = int(round(s_r / 255.0 * dr + o_r))
    _r = int(round((o_r + s_r) / 2.0))

    #green
    o_g = tuple(bank[_main].getpixel((x, y)))[1]
    dg = 255 - o_g
    # _g = int(round(s_g / 255.0 * dg + o_g))
    _g = int(round((o_g + s_g) / 2.0))

    #blue
    o_b = tuple(bank[_main].getpixel((x, y)))[2]
    db = 255 - o_b
    # _b = int(round(s_b / 255.0 * db + o_b))
    _b = int(round((o_b + s_b) / 2.0))

    return [int(round(norm(_r, q, 100))), int(round(norm(_g, q, 100))), int(round(norm(_b, q, 100)))]

    # x - main y - sub
    # (x.rgb + y.rgb) / 2

    #cos_func = lambda height, freq, x: height * math.cos(math.pi / (freq if freq != 0 else 1000) * x) / 2.0 + height / 2.0
    #sin_func = lambda height, freq, x: height * math.sin(math.pi / (freq if freq != 0 else 1000) * x) / 2.0 + height / 2.0

    #k = 5

    #iMain = int(round(sin_func(len(files) - 1, cos_func(len(files) - 1, 800 * k, y) * k, x)))
    #iSub = int(round(cos_func(len(files) - 1, sin_func(len(files) - 1, 600 * k, x) * k, y)))

    # iMain = int(round((len(files) - 1) * math.sin(math.pi / (math.cos(math.pi / 500 * y) if math.cos(math.pi / 500 * y) != 0 else 500) * x) / 2.0 + (len(files) - 1) / 2.0))
    # iSub = int(round((len(files) - 1) * math.cos(math.pi / (math.sin(math.pi / 800 * x) if math.sin(math.pi / 800 * x) != 0 else 800) * y) / 2.0 + (len(files) - 1) / 2.0))

    #m_r, m_g, m_b = bank[iMain].getpixel((x, y))
    #s_r, s_g, s_b = bank[iSub].getpixel((x, y))

    #return [int((m_r + s_r) / 2.0), int((m_g + s_g) / 2.0), int((m_b + s_b) / 2.0)]


def Generate(q = 1):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            pixel = GetPixelByPos(x, y, q)
            # canv.create_rectangle(x, y, x, y, outline=GetHex(pixel))
            image_to_save.putpixel((x, y), tuple(pixel))


def Save(name: str = ""):
    file = open('eq.txt', 'a')
    # file.write(f"n: {num_entry.get()}\n")
    # file.write(f"file: {ent.get()}\n")
    file.write("\n")
    file.close()
    # image_to_save.save(ent.get() + '.png')
    image_to_save.save(name + '.png')


def GetBank(_files: list) -> list:
    _bank = []
    for file in _files:
        _bank.append((Image.open("bank\\" + file)).convert('RGB'))
    return _bank


print("Starting...")

files = os.listdir(path='bank')
bank = GetBank(files)

WIDTH = bank[0].width
HEIGHT = bank[0].height

image_to_save = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))

upper_index = 2 ** 8 + 1

l1 = list(map(lambda x: round(x, 1), arange(0, 4, 0.1)))
l2 = list(range(4, upper_index, 4))

l = l1 + l2

for frame_index, q in enumerate(l):
    if (os.path.exists(f"destruction/frame{frame_index}.png")):
        print(f"Frame {frame_index} already done... {round((frame_index + 1) / len(l) * 100, 2)}%")
        continue

    Generate(q)
    Save(f"destruction/frame{frame_index}")
    print(f"Frame {frame_index} done with q = {q}... {round((frame_index + 1) / len(l) * 100, 2)}%")

# root = Tk()

# canv = Canvas(root,
#               width=WIDTH,
#               height=HEIGHT,
#               bg='white')
# # canv.grid(row=1, column=1, columnspan=2)

# num_label = Label(root,
#                   text="NUM: ")
# num_label.grid(row=2, column=1)

# num_entry = Entry(root, width=100)
# num_entry.grid(row=2, column=2)

# btn = Button(root,
#              text='Generate',
#              width=30,
#              height=5,
#              bg='white',
#              fg='black')
# btn.config(command=Generate)
# btn.grid(row=3, column=1, columnspan=2)

# ent = Entry(root,
#             width=30)
# ent.grid(row=4, column=1, columnspan=2)

# btn = Button(root,
#              text='Save',
#              width=30,
#              height=5,
#              bg='white',
#              fg='black')
# btn.config(command=Save)
# btn.grid(row=5, column=1, columnspan=2)
# root.mainloop()
