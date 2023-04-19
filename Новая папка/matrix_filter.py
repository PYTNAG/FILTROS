from PIL import Image
import math
import queue


class MatrixFilter:
    def __init__(self, src: Image, output: Image) -> None:
        self.src = src
        self.output = output

        self.max_r = 10.0
    
    def is_neutral(self, fc):
        pxl = self.src.getpixel(fc)
        return pxl[0] <= 25 and pxl[1] <= 25 and pxl[2] <= 25
    
    def in_bound(self, fc):
        return (0 <= fc[0] < self.src.width) and (0 <= fc[1] < self.src.height)

    def color(self) -> None:
        for buf_x in range(self.output.width):
            for buf_y in range(self.output.height):
                self.output.putpixel((buf_x, buf_y), self.get_color((buf_x, buf_y)))
            print(f"completed cols: {round((buf_x + 1) / self.output.width * 100, 2):06.2f} % | {buf_x + 1} / {self.output.width}")
    
    def get_color(self, fc):
        g = self.src.getpixel(fc)

        if self.is_neutral(fc):
            return g
        
        r = self.get_radius_factor(fc)

        rf = r / self.max_r
        
        gs = (g[0] + g[1] + g[2]) / 3.0

        k = rf * gs

        # _r = k / 2.0 * (math.sin(math.pi/25.0 * r) + 1)
        # _g = 0
        # _b = k / 2.0 * (math.cos(math.pi/25.0 * r) + 1)

        _r = k / 2.0 * (math.sin(math.pi/50.0 * r) + 1)
        _g = 0
        _b = k / 2.0 * (math.cos(math.pi/50.0 * r) + 1)

        return (round(_r), 0, round(_b))
    
    
    def get_radius_factor(self, fc):
        r = 1

        while r <= max(self.src.width, self.src.height):
            angles = [
                (fc[0] - r, fc[1] - r),
                (fc[0] + 0, fc[1] - r),
                (fc[0] + r, fc[1] - r),
                (fc[0] - r, fc[1] + 0),
                (fc[0] + r, fc[1] + 0),
                (fc[0] - r, fc[1] + r),
                (fc[0] + 0, fc[1] + r),
                (fc[0] + r, fc[1] + r),
            ]

            for a in angles:
                if self.in_bound(a) and self.is_neutral(a):
                    return r * math.sqrt(2)
            
            r += 1

    # def get_radius_factor(self, fc):
    #     q = queue.Queue()

    #     m = []

    #     q.put(fc)
    #     m.append(fc)

    #     r = []

    #     while q.qsize != 0:
    #         cur = q.get()

    #         if self.is_neutral(cur):
    #             r.append(cur)
            
    #         if len(r) == 0:
    #             for dx in range(-1, 2):
    #                 for dy in range(-1, 2):
    #                     if dx == 0 and dy == 0:
    #                         continue
                        
    #                     n = (cur[0] + dx, cur[1] + dy)
    #                     if self.in_bound(n) and n not in m:
    #                         q.put(n)
    #                         m.append(n)

        
    #     _min = min(r, key=lambda x: (x[0] - fc[0]) ** 2 + (x[1] - fc[1]) ** 2)

    #     return ((_min[0] - fc[0]) ** 2 + (_min[1] - fc[1]) ** 2) ** 0.5

