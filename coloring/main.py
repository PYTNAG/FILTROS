from PIL import Image

from args import Arguments
from matrix_filter import MatrixFilter

import sys
import os


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


def save_to_heap(image: Image, image_name: str) -> None:
    i = 0
    ext = image_name.split('.')[1]

    if not os.path.exists('heap'):
        os.mkdir('heap')
    
    while os.path.exists(f"heap\\converted_{i}.{ext}"):
        i += 1
    
    image.save(f"heap\\converted_{i}.{ext}")


def color_filter(filename) -> Image:
    src = Image.open(filename).convert('RGB')
    output = Image.new('RGB', src.size)

    m_filter = MatrixFilter(src, output)

    try:
        m_filter.color()
    except Exception as e:
        print(e)
    finally:
        return output


if __name__ == '__main__':
    args = Arguments()
    args.parse(sys.argv[1:])

    args.add_association(('-s', '--size'))

    img_path = args.get_value('-f')
    if img_path:
        img_path = img_path[0]
        image = color_filter(img_path)
        if image != None:
            save_to_heap(image, img_path) if args.get_value('-h') else save_image(image, "", img_path)
            print('\a')
    del img_path
