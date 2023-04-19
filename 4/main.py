import tkinter
import os
from App import *
from DigitalArtist import *
from HexColor import *


def draw():
    global artist
    global app
    r_f = app.get_widget('e_red').get()
    g_f = app.get_widget('e_green').get()
    b_f = app.get_widget('e_blue').get()
    a_f = app.get_widget('e_alpha').get()
    artist.draw_with_func(r_f, g_f, b_f, a_f)
    # canvas = app.get_widget('canvas')

    # artist.save_image("tmp.png")
    # canvas.create_image(0, 0, image=tkinter.PhotoImage(file="tmp.png"), anchor=tkinter.NW)
    # os.remove("tmp.png")


def save():
    r_f = app.get_widget('e_red').get()
    g_f = app.get_widget('e_green').get()
    b_f = app.get_widget('e_blue').get()
    a_f = app.get_widget('e_alpha').get()
    name = app.get_widget('e_name').get()

    file = open('eq.txt', 'a')
    file.write(f"r: {r_f}\n")
    file.write(f"g: {g_f}\n")
    file.write(f"b: {b_f}\n")
    file.write(f"a: {a_f}\n")
    file.write(f"file: {name}.png\n")
    file.write("\n")
    file.close()

    artist.save_image(f"{name}.png")


def add_field(
        l_name: str,
        e_name: str,
        l_text: str,
        row: int
             ) -> None:
    app.add_widget(
        l_name,
        app.get_label(l_text),
        row, 1
    )
    app.add_widget(
        e_name,
        app.get_entry(),
        row, 2
    )


WIDTH, HEIGHT = 1500, 1500

artist = Artist('RGB', (WIDTH, HEIGHT))
app = App("Digital Artist")

# app.add_widget(
#     'canvas',
#     app.get_canvas(WIDTH, HEIGHT, RGBColor.white),
#     1, 1, 2
# )

add_field('l_red', 'e_red', 'RED: ', 1)
add_field('l_green', 'e_green', 'GREEN: ', 2)
add_field('l_blue', 'e_blue', 'BLUE: ', 3)
add_field('l_alpha', 'e_alpha', 'ALPHA: ', 4)

app.add_widget(
    'btn_draw',
    app.get_button('Draw', (30, 5)),
    5, 1, 2
)
app.set_button_command('btn_draw', draw)

add_field('l_name', 'e_name', 'NAME: ', 6)
app.add_widget(
    'btn_save',
    app.get_button('Save', (30, 5)),
    7, 1, 2
)
app.set_button_command('btn_save', save)

app.start()
