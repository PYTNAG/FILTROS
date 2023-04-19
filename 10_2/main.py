from PIL import Image
import numpy as np

from args import Arguments
from matrix_filter import MatrixFilter

import sys
import os
import random


def get_image(path: str) -> Image:
    return Image.open(path).convert('RGB')


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


def substruct_filter(image: Image, size: int, is_mask) -> Image:
    result_image = Image.new('RGB', (image.width - size + 1, image.height - size + 1), (0, 0, 0))
    m_filter = MatrixFilter(image, result_image, size)

    m_filter.complete_image_substruct(is_mask)
    
    return result_image


def contour_filter(image: Image, size: int, center: tuple[int, int], radius: float) -> Image:
    result_image = Image.new('RGB', (image.width - size + 1, image.height - size + 1), (0, 0, 0))
    m_filter = MatrixFilter(image, result_image, size)

    m_filter.complete_image_contour(center, radius)
    
    return result_image


def apply(image: Image, args: Arguments) -> Image:
    size_arg = args.get_value('-s')
    is_contour = args.get_value('--contour')
    if size_arg:
        size = int(size_arg[0])
        if size % 2 == 0:
            raise Exception('Size must be odd')
        
        if is_contour:
            center = list(map(lambda x: int(x), args.get_value('--center')))
            radius = float(args.get_value('-r')[0])

            return contour_filter(image, size, center, radius)
        else:
            return substruct_filter(image, size, args.get_value('-m'))


if __name__ == '__main__':
    args = Arguments()
    args.parse(sys.argv[1:])

    args.add_association(('-s', '--size'))

    args.add_association(('-f', '--file'))

    args.add_association(('-h', '--heap'))

    args.add_association(('-m', '--mask'))

    args.add_association(('-r', '--radius'))

    img_path = args.get_value('-f')
    if img_path:
        img_path = img_path[0]
        image = get_image(img_path)
        image = apply(image, args)
        if image != None:
            save_to_heap(image, img_path) if args.get_value('-h') else save_image(image, "", img_path)
    del img_path
