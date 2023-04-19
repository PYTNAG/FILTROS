from PIL import Image
from indexedPalette import IndexedPalette

from args import Arguments

import sys
import os

def get_image(path: str) -> Image:
    return Image.open(path).convert('RGBA')


def index_image(image: Image, palette: IndexedPalette) -> Image:
    result_image = Image.new('RGBA', (image.width, image.height), (0, 0, 0, 1))

    for x in range(image.width):
        for y in range(image.height):
            src_pxl = image.getpixel((x, y))
            pixel = palette.index_color(src_pxl)
            result_image.putpixel((x, y), pixel)
        print(f"completed rows: {x + 1} / {image.width} [{(x + 1) / image.width * 100:06.2f}%]")
    
    return result_image


def save_image(image: Image, image_folder: str, image_name: str) -> None:
    i = 0

    name = image_name.split('.')[0]

    if image_folder == "":
        if not os.path.exists(name):
            os.mkdir(name)
        save_path = lambda i: f"{name}\\converted_{i}.png"
    else:
        if not os.path.exists(f"{image_folder}\\{image_folder.split('/')[-1]}_conv"):
            os.mkdir(f"{image_folder}\\{image_folder.split('/')[-1]}_conv")
        save_path = lambda i: f"{image_folder}\\{image_folder.split('/')[-1]}_conv\\converted_{i}.png"

    while os.path.exists(save_path(i)):
        i += 1
    
    image.save(save_path(i))


def save_to_heap(image: Image) -> None:
    i = 0

    if not os.path.exists('heap'):
        os.mkdir('heap')
    
    while os.path.exists(f"heap\\converted_{i}.png"):
        i += 1
    
    image.save(f"heap\\converted_{i}.png")


def apply(image: Image, args: Arguments) -> Image:
    wings = args.get_value('-w')
    if wings:
        palette = IndexedPalette()
        
        for wing in wings:
            palette.add_wing_hex(wing)

        return index_image(image, palette)
    else:
        raise TypeError('You should set -w (--wings) flag')


if __name__ == '__main__':
    args = Arguments()
    args.parse(sys.argv[1:])

    args.add_association(('-w', '--wings'))

    args.add_association(('-f', '--file'))

    args.add_association(('-h', '--heap'))

    img_path = args.get_value('-f')
    if img_path:
        img_path = img_path[0]
        image = get_image(img_path)
        image = apply(image, args)
        if image != None:
            save_to_heap(image) if args.get_value('-h') else save_image(image, "", img_path)
