from PIL import Image, ImageDraw
from HexColor import *


class Artist:
    def __init__(self, mode: str, size: tuple):
        self.__mode = mode
        self.__size = size
        if mode == 'RGB':
            self.__canvas = Image.new(mode='RGB', size=size, color=RGBColor.white.get_rgb())
        else:
            raise ValueError('unknown mode')

    def save_image(self, path: str):
        self.__canvas.save(path)

    def draw_with_func(self,
                       r_func: str,
                       g_func: str,
                       b_func: str,
                       a_func: str):
        import math
        draw = ImageDraw.Draw(self.__canvas)
        for x in range(self.__size[0]):
            for y in range(self.__size[1]):
                old_r, old_g, old_b = self.__canvas.getpixel((x, y))

                r = self.__to_byte(round(eval(r_func)))
                g = self.__to_byte(round(eval(g_func)))
                b = self.__to_byte(round(eval(b_func)))
                a = eval(a_func)

                _r = self.__to_byte(round(r*a + old_r*(1-a)))
                _g = self.__to_byte(round(g*a + old_g*(1-a)))
                _b = self.__to_byte(round(b*a + old_b*(1-a)))

                color = HexRGB(_r, _g, _b).get_rgb()
                draw.point([x, y], fill=color)

    def clear_canvas(self):
        if self.__mode == 'RGB':
            self.__canvas = Image.new(mode='RGB', size=self.__size, color=RGBColor.white.get_rgb())
        elif self.__mode == 'RGBA':
            self.__canvas = Image.new(mode='RGBA', size=self.__size, color=RGBAColor.white.get_rgba())

    @staticmethod
    def __to_byte(n: int) -> int:
        if n >= 255:
            return 255
        elif n <= 0:
            return 0
        else:
            return n

    def get_canvas(self) -> Image:
        return self.__canvas
