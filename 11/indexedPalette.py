import math

class IndexedPalette:
    def __init__(self) -> None:
        self.wings = []
        self.metric = lambda v3: v3[0] ** 2 + v3[1] ** 2 + v3[2] ** 2
    
    def add_wing_rgb(self, rgb):
        self.wings.append(rgb)

    def add_wing_hex(self, hex):
        if hex[0] == '#':
            hex = hex[1:]
        
        self.add_wing_rgb((
            int(hex[0:2], base=16),
            int(hex[2:4], base=16),
            int(hex[4:], base=16)
            ))
    
    def index_color(self, rgb):
        nearest_wing = (0, 0, 0)
        nearest_cos = 0.0

        for wing in self.wings:
            cos = self.cos(wing, rgb)
            if cos >= nearest_cos:
                nearest_cos = cos
                nearest_wing = wing
        
        k = nearest_cos * math.sqrt(self.d2(rgb) / self.d2(nearest_wing))

        return (
            round(nearest_wing[0] * k * 2) // 2,
            round(nearest_wing[1] * k * 2) // 2,
            round(nearest_wing[2] * k * 2) // 2,
        )
    
    def cos(self, v1, v2):
        dot_prod = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

        met_prod = math.sqrt(self.d2(v1) * self.d2(v2))

        return dot_prod / met_prod if met_prod != 0 else 0
    
    @staticmethod
    def d2(v):
        return v[0] ** 2 + v[1] ** 2 + v[2] ** 2