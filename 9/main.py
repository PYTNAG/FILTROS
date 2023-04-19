from PIL import Image
from indexedPalette import IndexedPalette
import normalizer

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
            if src_pxl[3] == 0:
                result_image.putpixel((x, y), (166, 235, 201))
            else:
                pixel = palette.index_color(src_pxl)
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


def save_to_heap(image: Image, image_name: str) -> None:
    i = 0

    if not os.path.exists('heap'):
        os.mkdir('heap')
    
    while os.path.exists(f"heap\\converted_{i}.png"):
        i += 1
    
    image.save(f"heap\\converted_{i}.png")


def apply(image: Image, args: Arguments) -> Image:
    norm_arg = args.get_value('-n')
    if norm_arg:
        return normalize_image(image, (int(norm_arg[0]), int(norm_arg[1]), int(norm_arg[2])))
    del norm_arg

    index_args = args.get_value('-i')
    if index_args:
        palette = IndexedPalette()

        counter = 0
        for color in index_args:
            match color[0]:
                case '!':
                    palette.add_ignore(color.replace('!', "#"))
                case '#':
                    palette.add_color(color, counter)
                    counter += 1
                case '$':
                    palette.add_static(color.replace('$', '#'))
                case _:
                    raise Exception("Unknown hex-prefix")
        
        return index_image(image, palette)
    del index_args

    auto = args.get_value('--auto')
    if auto:
        palette = IndexedPalette()

        bank_arg = args.get_value('-b')
        folder = f"{bank_arg[0]}\\" if bank_arg else ""

        colors = list(filter(lambda line: line != '\n' and not line.startswith('//'), open(f'{folder}colors.txt').readlines()))

        counter = 0
        for color in colors:
            color = color.removesuffix('\n')
            match color[0]:
                case '!':
                    palette.add_ignore(color.replace('!', "#"))
                case '#':
                    palette.add_color(color, counter)
                    counter += 1
                case '$':
                    palette.add_static(color.replace('$', '#'))
                case _:
                    raise Exception("Unknown hex-prefix")
        
        return index_image(image, palette)
    del auto

    return None


if __name__ == '__main__':
    args = Arguments()
    args.parse(sys.argv[1:])

    args.add_association(('-i', '--index'))
    args.add_association(('-n', '--normalize'))
    args.add_association(('-s', '--star'))

    args.add_association(('-f', '--file'))
    args.add_association(('-b', '--bank'))

    args.add_association(('-h', '--heap'))

    img_path = args.get_value('-f')
    if img_path:
        img_path = img_path[0]
        image = get_image(img_path)
        image = apply(image, args)
        if image != None:
            save_to_heap(image, img_path) if args.get_value('-h') else save_image(image, "", img_path)
    del img_path

    bank_path = args.get_value('-b')
    if bank_path:
        bank_path = bank_path[0]
        files = os.listdir(path=bank_path)
        for file in files:
            if not file.endswith(('.png', '.jpg', '.jpeg')):
                continue
            image = get_image(f"{bank_path}\\{file}")
            image = apply(image, args)
            if image != None:
                save_to_heap(image, file) if args.get_value('-h') else save_image(image, bank_path, file)
    del bank_path
