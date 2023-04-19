import math

class MatrixFilter:
    def __init__(self, src, output) -> None:
        self.src = src
        self.output = output

        self.upper_border = 0
        self.lower_border = 0
        self.going_throw = False

        self.ticks = 0
    
    def tick(self):
        self.ticks += 1

        # if self.ticks % 10 == 0 or self.ticks == self.src.width:
        print(f"completed cols: {round((self.ticks) / self.src.width * 100, 2):06.2f} % | {self.ticks} / {self.src.width}")
    
    def in_bound(self, fc):
        return (0 <= fc[0] < self.src.width) and (0 <= fc[1] < self.src.height)

    def is_black(self, color):
        return \
            self.is_near(color, (29, 95, 127), (50, 50, 50)) or \
            self.is_near(color, (0, 0, 0), (20, 20, 20))
    
    @staticmethod
    def is_near(color, kernel, precision):
        return \
            (abs(color[0] - kernel[0]) <= precision[0]) and \
            (abs(color[1] - kernel[1]) <= precision[1]) and \
            (abs(color[2] - kernel[2]) <= precision[2])

    def color(self) -> None:
        for buf_x in range(self.src.width):
            for buf_y in range(self.src.height):
                self.output.putpixel((buf_x, buf_y), self.get_color((buf_x, buf_y)))
            self.tick()
    

    def get_color(self, fc):
        src_color = self.src.getpixel(fc)
        if self.is_black(src_color):
            if self.is_near(src_color, (29, 95, 127), (50, 50, 50)):
                return (29, 95, 127)
            else:
                return (0, 0, 0)
        
        is_upper_found = False
        is_lower_found = False
        
        if self.going_throw:
            is_upper_found = True
            is_lower_found = True

            self.upper_border += 1
            self.lower_border -= 1
            if self.lower_border == 0:
                self.going_throw = False

        while not (is_upper_found and is_lower_found):
            if not is_upper_found:
                upper = (fc[0], fc[1] - self.upper_border)
                if not self.in_bound(upper) or self.is_black(self.src.getpixel(upper)):
                    is_upper_found = True
                else:
                    self.upper_border += 1
            
            if not is_lower_found:
                lower = (fc[0], fc[1] + self.lower_border)
                if not self.in_bound(lower) or self.is_black(self.src.getpixel(lower)):
                    is_lower_found = True
                else:
                    self.lower_border += 1
        
        if not self.going_throw and self.lower_border > 0:
            self.going_throw = True

        # upper_anchor = 1000
        # lower_anchor = 1000

        # red_q = self.upper_border / upper_anchor if self.upper_border < upper_anchor else 1
        # green_q = self.lower_border / lower_anchor if self.lower_border < lower_anchor else 1

        s = self.upper_border + self.lower_border
        d = self.upper_border

        q = d / s

        if not self.going_throw:
            self.upper_border = 0
            self.lower_border = 0

        return (
            round( 255 * self.g_q(q) ),
            round( 255 * self.r_q(q) ),
            100
        )

    def r_q(self, q):
        k = 5/4
        return k * q if q <= 1/k else 1

    def g_q(self, q):
        k = 20/19
        return 1 if q <= 1 - 1/k else k * (1 - q)

