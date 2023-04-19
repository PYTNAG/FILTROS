class B3:
    def __init__(self, r: int, g: int, b: int) -> None:
        if 0 >= r >= 255 or 0 >= g >= 255 or 0 >= b >= 255:
            raise Exception('R, G, B components must be bytes')
        
        self.r = r
        self.g = g
        self.b = b
    
    def distance_to(self, other) -> float:
        return ((self.r - other.r) ** 2 + (self.g - other.g) ** 2 + (self.b - other.b) ** 2) ** 0.5
    
    def tuple(self):
        return (self.r, self.g, self.b)


class B3_Factor:
    def __init__(self, c: B3) -> None:
        self.dr = 0
        self.dg = 0
        self.db = 0

        factor = 0
        for dr in [0, 1]:
            for dg in [0, 1]:
                for db in [0, 1]:
                    corner = B3(dr * 255, dg * 255, db * 255)
                    if c.distance_to(corner) > factor:
                        self.dr = dr - c.r
                        self.dg = dg - c.g
                        self.db = db - c.b
    
    def value(self):
        return (self.dr ** 2 + self.dg ** 2 + self.db ** 2) ** 0.5


class Normalizer:
    def __init__(self) -> None:
        pass

    def norm_pixel(self, v3: B3, c: B3, factor: B3_Factor) -> B3:
        # r_n = self.norm_component(v3.r, c.r, factor.dr)
        # g_n = self.norm_component(v3.g, c.g, factor.dg)
        # b_n = self.norm_component(v3.b, c.b, factor.db)

        # d = c.distance_to(v3)
        # k = (d / factor.value()) ** 1
        black = B3(0, 0, 0)
        white = B3(255, 255, 255)
        max_d = white.distance_to(black)
        
        k = (factor.value() / max_d)

        gray = (v3.r + v3.g + v3.b) / 3.0

        r_n = int(round(v3.r + k * (gray - v3.r)))
        g_n = int(round(v3.g + k * (gray - v3.g)))
        b_n = int(round(v3.b + k * (gray - v3.b)))
        
        return (r_n, g_n, b_n)

    def norm_component(self, r, cr, fdr):
        dr = r - cr

        if dr == 0:
            return r
        
        if dr > 0:
            return int(255 - round(dr / fdr * (255 - r)))
        else:
            return int(round(dr / fdr * r))

        # if dr > 0:
        #     return int(round(r + dr / fdr * (255 - r)))
        # else:
        #     return int(round(r - dr / fdr * r))