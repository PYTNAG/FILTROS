def is_byte(x: int) -> bool:
    return 0 <= x <= 255


class IndexedPalette:
    def __init__(self) -> None:
        self.colors = {}
        self.ignore = []
        self.static = []
        self.metric = lambda v3: v3[0] ** 2 + v3[1] ** 2 + v3[2] ** 2
    
    def add_ignore(self, rgb) -> None:
        if type(rgb) is str:
            rgb = self.parse_hex(rgb)
        
        self.ignore.append(rgb)
    
    def add_static(self, rgb) -> None:
        if type(rgb) is str:
            rgb = self.parse_hex(rgb)
        
        self.static.append(rgb)

    def add_color(self, rgb, priority: int) -> None:
        if type(rgb) is str:
            rgb = self.parse_hex(rgb)
        
        if not is_byte(rgb[0]) or not is_byte(rgb[1]) or not is_byte(rgb[2]):
            raise Exception('Invalid RGB tuple')
        
        if priority in self.colors:
            raise Exception('Color with given priority already exist')

        self.colors[priority] = rgb
    
    @staticmethod
    def parse_hex(hex: str) -> tuple[int, int, int]:
        if hex[0] != '#' or len(hex) != 7:
            raise Exception(f'Wrong hex-code ({hex}) for color (Must be like #RRGGBB)')
        
        return (int(hex[1:3], base=16), int(hex[3:5], base=16), int(hex[5:], base=16))
    
    def set_metric(self, v3_metric) -> None:
        try:
            test = float(v3_metric((0, 0, 0)))

            self.metric = v3_metric
        except:
            raise Exception('Wrong metric')
    
    def index_color(self, rgb) -> tuple[int, int, int]:
        if type(rgb) is str:
            rgb = self.parse_hex(rgb)

        if rgb in self.ignore:
            return rgb

        # priority : distance : color_rgb
        index = (-1, -1, (0, 0, 0))

        for priority in self.colors:
            color = self.colors[priority]
            dr = rgb[0] - color[0]
            dg = rgb[1] - color[1]
            db = rgb[2] - color[2]

            q_dist = self.metric((dr, dg, db))

            if (index[1] == -1 or index[1] > q_dist or (index[1] == q_dist and index[0] < priority)):
                index = (priority, q_dist, color)
        
        for s in self.static:
            dr = rgb[0] - s[0]
            dg = rgb[1] - s[1]
            db = rgb[2] - s[2]

            q_dist = self.metric((dr, dg, db))

            if (index[1] == -1 or index[1] > q_dist):
                index = (priority, q_dist, s)
        
        return index[2] if index[2] not in self.static else rgb