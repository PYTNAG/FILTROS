from PIL import Image
from indexedPalette import IndexedPalette
import normalizer

import sys
import os

def get_image(path: str) -> Image:
    return Image.open(path).convert('RGB')


def index_image(image: Image, palette: IndexedPalette) -> Image:
    result_image = Image.new('RGB', (image.width, image.height), (0, 0, 0))

    for x in range(image.width):
        for y in range(image.height):
            pixel = palette.index_color(image.getpixel((x, y)))
            result_image.putpixel((x, y), pixel)
    
    return result_image


def normalize_image(image: Image, c: tuple[int, int, int]) -> Image:
    result_image = Image.new('RGB', (image.width, image.height), (0, 0, 0))

    n = normalizer.Normalizer()

    center = normalizer.B3(c[0], c[1], c[2])
    fc = normalizer.B3_Factor(center)
    
    for x in range(image.width):
        for y in range(image.height):
            src = image.getpixel((x, y))
            v3 = normalizer.B3(src[0], src[1], src[2])
            pixel = n.norm_pixel(v3, center, fc)
            result_image.putpixel((x, y), pixel)
    
    return result_image


def save_image(image: Image, image_folder: str, image_name: str) -> None:
    i = 0

    name = image_name.split('.')[0]
    ext = image_name.split('.')[1]

    if image_folder == "":
        if not os.path.exists(name):
            os.mkdir(name)
        save_path = lambda i: f"{name}\\converted_{i}.{ext}"
    else:
        if not os.path.exists(f"{image_folder}\\{name}"):
            os.mkdir(f"{image_folder}\\{name}")
        save_path = lambda i: f"{image_folder}\\{name}\\converted_{i}.{ext}"

    while os.path.exists(save_path(i)):
        i += 1
    
    image.save(save_path(i))


def apply(image: Image) -> Image:
    if len(sys.argv) > 3 and sys.argv[3] == '-n':
        return normalize_image(image, eval(sys.argv[4]))
    else:
        palette = IndexedPalette()

        palette.add_ignore("#FFFFFF")

        palette.add_color("#D00000", 0)
        # palette.add_color("#FEA82F", 1)
        # palette.add_color("#FFFFFF", -1)
        # palette.add_color("#071013", 3)
        palette.add_color("#FF4D00", 4)

        return index_image(image, palette)


if __name__ == '__main__':
    if sys.argv[1] in {'-f', '--file'} :
        image = get_image(sys.argv[2])
        save_image(apply(image), "", sys.argv[2])

    
    if sys.argv[1] in {'-b', '--bank'} :
        files = os.listdir(path=sys.argv[2])
        for file in files:
            image = get_image(f"{sys.argv[2]}\\{file}")
            save_image(apply(image), sys.argv[2], file)
