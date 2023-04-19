class HexRGB:
    def __init__(self, r: int, g: int, b: int):
        if self.is_byte(r) and self.is_byte(g) and self.is_byte(b):
            self.__r = r
            self.__g = g
            self.__b = b
        else:
            raise ValueError("R, G and B components must be bytes (non-negative and less than 256)")

    def get_hex(self) -> str:
        r_hex = self.__get_hex_value(self.__r)
        g_hex = self.__get_hex_value(self.__g)
        b_hex = self.__get_hex_value(self.__b)
        return f"#{r_hex}{g_hex}{b_hex}"

    def get_rgb(self) -> tuple:
        return self.__r, self.__g, self.__b

    @staticmethod
    def __get_hex_value(byte: int):
        _hex = hex(byte)[2:]
        if len(_hex) == 1:
            return '0' + _hex
        return _hex

    @staticmethod
    def is_byte(n: int) -> bool:
        return 0 <= n <= 255


class HexRGBA(HexRGB):

    def __init__(self, r: int, g: int, b: int, a: float):
        super().__init__(r, g, b)
        if 0 <= a <= 1:
            self.__a = a
        else:
            raise ValueError('Alpha channel must be non-negative and less or equal 1')

    def get_hex(self) -> str:
        r_hex = self.__get_hex_value(self.__r)
        g_hex = self.__get_hex_value(self.__g)
        b_hex = self.__get_hex_value(self.__b)
        a_hex = self.__get_hex_value(round(self.__a * 255))
        return f"#{r_hex}{g_hex}{b_hex}{a_hex}"

    def get_rgba(self) -> tuple:
        return super().get_rgb() + (round(self.__a * 255), )


class RGBColor:
    white = HexRGB(255, 255, 255)
    black = HexRGB(0, 0, 0)
    red = HexRGB(255, 0, 0)
    green = HexRGB(0, 255, 0)
    blue = HexRGB(0, 0, 255)


class RGBAColor:
    white = HexRGBA(255, 255, 255, 1)
    black = HexRGBA(0, 0, 0, 1)
    red = HexRGBA(255, 0, 0, 1)
    green = HexRGBA(0, 255, 0, 1)
    blue = HexRGBA(0, 0, 255, 1)
