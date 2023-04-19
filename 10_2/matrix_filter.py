from PIL import Image
import enum


class COMPONENT(enum.Enum):
    R = 0,
    G = 1,
    B = 2,


class MatrixFilter:
    def __init__(self, src: Image, output: Image, size: int) -> None:
        self.src = src
        self.output = output

        self.size = size
        self.delta = int((size - 1) / 2)
    
    def complete_image_contour(self, center, radius) -> None:
        self.center = center
        self.radius = radius

        for buf_x in range(self.output.width):
            for buf_y in range(self.output.height):
                self.output.putpixel((buf_x, buf_y), self.complete_block_contour((buf_x, buf_y)))
            print(f"completed cols: {round((buf_x + 1) / self.output.width * 100, 2)} % | {buf_x + 1} / {self.output.width}")
    
    def complete_image_substruct(self, is_mask) -> None:
        for buf_x in range(self.output.width):
            for buf_y in range(self.output.height):
                self.output.putpixel((buf_x, buf_y), self.complete_block_substruct((buf_x, buf_y), is_mask))
            print(f"completed cols: {round((buf_x + 1) / self.output.width * 100, 2)} % | {buf_x + 1} / {self.output.width}")
    
    def contour_include(self, point):
        sq_dist = (point[0] - self.center[0]) ** 2 + (point[1] - self.center[1]) ** 2
        return sq_dist <= self.radius ** 2

    def complete_block_contour(self, point: tuple[int, int]) -> tuple[int, int, int]:
        res_pixel = (0, 0, 0)
        
        kernel = (point[0] + self.delta, point[1] + self.delta)

        if self.contour_include(kernel):
            return self.src.getpixel(kernel)

        for dx in range(self.size):
            for dy in range(self.size):
                cell_point = (point[0] + dx, point[1] + dy)
                cell_pixel = self.src.getpixel(cell_point)

                if dx == dy == self.delta:
                    res_pixel = (
                        res_pixel[0] + cell_pixel[0],
                        res_pixel[1] + cell_pixel[1],
                        res_pixel[2] + cell_pixel[2]
                    )
                    continue
                
                f_cb = (
                    cell_point[0] - kernel[0],
                    cell_point[1] - kernel[1]
                )
                cf_b = (
                    self.center[0] - kernel[0],
                    self.center[1] - kernel[1]
                )

                corr = f_cb[0] * cf_b[0] + f_cb[1] * cf_b[1]
                cos_corr = corr / (((f_cb[0] ** 2 + f_cb[1] ** 2) * (cf_b[0] ** 2 + cf_b[1] ** 2)) ** 0.5)

                res_pixel = (
                    res_pixel[0] + int(round(cell_pixel[0] * cos_corr / 2)),
                    res_pixel[1] + int(round(cell_pixel[1] * cos_corr / 2)),
                    res_pixel[2] + int(round(cell_pixel[2] * cos_corr / 2))
                )
        
        return res_pixel
    
    def complete_block_substruct(self, point: tuple[int, int], is_mask) -> tuple[int, int, int]:
       res_pixel = [0, 0, 0]
       max_delta = [0, 0, 0]
       
       kernel = self.src.getpixel((point[0] + self.delta, point[1] + self.delta))
    
       for dx in range(self.size):
           for dy in range(self.size):
               
               if dx == dy == self.delta:
                   continue
               
               cell_pixel = self.src.getpixel((point[0] + dx, point[1] + dy))
    
               magma = [
                   cell_pixel[0] - kernel[0],
                   cell_pixel[1] - kernel[1],
                   cell_pixel[2] - kernel[2]
               ]
    
               res_pixel[0] += magma[0]
               res_pixel[1] += magma[1]
               res_pixel[2] += magma[2]
               
               max_delta[0] = max_delta[0] if magma[0] < max_delta[0] else magma[0]
               max_delta[1] = max_delta[1] if magma[1] < max_delta[1] else magma[1]
               max_delta[2] = max_delta[2] if magma[2] < max_delta[2] else magma[2]
       
       out = [
           int(round(255 * res_pixel[0] / max_delta[0])) if max_delta[0] != 0 else 0, 
           int(round(255 * res_pixel[1] / max_delta[1])) if max_delta[1] != 0 else 0, 
           int(round(255 * res_pixel[2] / max_delta[2])) if max_delta[2] != 0 else 0
       ]
    
       if is_mask:
           return tuple(out)
       
       return kernel if out == [0, 0, 0] else tuple(out)