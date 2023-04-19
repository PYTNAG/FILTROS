import math

class MatrixFilter:
    def __init__(self, src, output) -> None:
        self.src = src
        self.output = output

        self.ticks = 0
    
    def tick(self):
        self.ticks += 1

        if self.ticks % 10 == 0 or self.ticks == self.src.width:
            print(f"completed cols: {round((self.ticks) / self.src.width * 100, 2):06.2f} % | {self.ticks} / {self.src.width}")
    
    def in_bound(self, fc):
        return (0 <= fc[0] < self.src.width) and (0 <= fc[1] < self.src.height)

    def color(self) -> None:
        for buf_x in range(self.src.width):
            for buf_y in range(self.src.height):
                self.output.putpixel((buf_x, buf_y), self.get_color((buf_x, buf_y)))
            self.tick()
    

    def get_color(self, fc):
        g = self.src.getpixel(fc)

        addition = [0, 0, 0]
        r = 25

        # for dt in range(0, r+1):
        for dt in range(-r, r+1):
            i = dt / r
            c = (898, 1119)

            # dot = (
            #     round(c[0] + i * (fc[0] - c[0])), 
            #     round(c[1] + i * (fc[1] - c[1]))
            #     # round(fc[1] - 0.38 / 2 * (dt - fc[0]))
            # )

            # dot = (
            #     round(fc[0] + i * c[0]),
            #     round(fc[1] + i * c[1])
            # )

            dot = (
                round(fc[0] + dt),
                round(fc[1] + 1 / 50 * (dt - fc[1]))
            )

            try:
                a = self.src.getpixel(dot)
                w = self.t_weight(dt)

                sign = -1
                            
                addition[0] += sign * w * (a[0] - g[0])
                addition[1] += sign * w * (a[1] - g[1])
                addition[2] += sign * w * (a[2] - g[2])
            except IndexError:
                continue

        return (
            (g[0] + round(addition[0])) % 256,
            (g[1] + round(addition[1])) % 256,
            (g[2] + round(addition[2])) % 256,
        )
    
    # @staticmethod
    # def t_weight(t):
    #     return math.exp(-abs(t)/2.2) / 10

    @staticmethod
    def t_weight(t):
        return abs(math.sin(t/10) * (math.cos(t/10) + 1) / 20)
