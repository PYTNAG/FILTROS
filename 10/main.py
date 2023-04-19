from PIL import Image

from args import Arguments

import sys
import os
import math

def draw_calc(centers, hb, vb, size) -> Image :
    res_image = Image.new('RGB', size, (255, 255, 255))

    x_step = (hb[1] - hb[0]) / float(size[0])
    x_offset = x_step / 2.0
    
    y_step = (vb[1] - vb[0]) / float(size[1])
    y_offset = y_step / 2.0

    values = []
    min = None
    max = None

    print("calculating values...")
    all = size[0] * size[1]

    for x in range(size[0]):
        values.append([])
        for y in range(size[1]):
            # z = (
            #     hb[0] + x_offset + x * x_step,
            #     vb[0] + y_offset + y * y_step
            # )

            z = (
                hb[0] + x * x_step,
                vb[0] + y * y_step
            )

            values[x].append(f(z, centers))
            if max is None or values[x][y] > max:
                max = values[x][y]
            if min is None or values[x][y] < min:
                min = values[x][y]

            # print(f"[{z[0]:5.2f}, {z[1]:5.2f}] = {values[x][y]}: {x * size[0] + y} / {all} ({round(100 * (x * size[0] + y) / float(all), 4):.4f}%)")
    print("complete.")

    print(f"min/max : {min}/{max}")
    
    print("\ndrawing...")

    prime_color = (244, 184, 96)
    second_color = (200, 62, 77)

    for x in range(size[0]):
        for y in range(size[1]):
            k = (values[x][y] - min) / (max - min)
            d = 5.0

            kd = math.floor((d + 1) * k) / d
            
            r = round(prime_color[0] * kd + second_color[0] * (1 - kd))
            g = round(prime_color[1] * kd + second_color[1] * (1 - kd))
            b = round(prime_color[2] * kd + second_color[2] * (1 - kd))

            res_image.putpixel((x, y), (r, g, b))

    print("complete.")
    return res_image


def f(z, cs) -> float:
    z2 = (
        z[0] ** 2 - z[1] ** 2,
        2 * z[0] * z[1]
    )

    min_sq = None
    for c in cs:
        d_sq = (z2[0] - c[0]) ** 2 + (z2[1] - c[1]) ** 2
        if min_sq is None or d_sq < min_sq:
            min_sq = d_sq

    return min_sq ** 0.5

    # d = 1.0
    # for c in cs:
    #     d *= ((z[0] - c[0]) ** 2 + (z[1] - c[1]) ** 2) ** 0.5
    
    # return d ** (2.0 / len(cs))

    # d = 0.0
    # for c in cs:
    #     d += ((z[0] - c[0]) ** 2 + (z[1] - c[1]) ** 2) ** 0.5
    
    # return d

    # return 1 + math.sin(z[0]) * math.sin(z[1]) * math.sin(z[0] * z[1]) / (2 * z[0] * z[1]) if z[0] != 0 and z[1] != 0 else 1

    # k = math.cos(math.sqrt(z[0] ** 2 + z[1] ** 2)) / math.sqrt(z[0] ** 2 + z[1] ** 2) if (z[0] != 0 or z[1] != 0) else 0
    # return math.sqrt((z[0] * k) ** 2 + (z[1] * k) ** 2)


def draw_grad(centers, hb, vb, size) -> Image :
    res_image = Image.new('RGB', size, (255, 255, 255))

    x_step = (hb[1] - hb[0]) / float(size[0])
    y_step = (vb[1] - vb[0]) / float(size[1])

    values = []
    max_grad = None

    print("calculating values...")

    for x in range(size[0]):
        values.append([])
        for y in range(size[1]):
            z = (
                hb[0] + x * x_step,
                vb[0] + y * y_step
            )

            grad = nabla(z, centers)
            measure = math.sqrt(grad[0] ** 2 + grad[1] ** 2)

            rc0 = get_rc0(grad)

            values[x].append(rc0)
            if max_grad is None or measure > max_grad:
                max_grad = measure

    print("complete.")
    
    print("\ndrawing...")

    for x in range(size[0]):
        for y in range(size[1]):
            rc0 = values[x][y]
            rc = list(map(lambda x: round(x / max_grad), rc0))

            d = 10.0

            rc = list(map(lambda x: round(255 / d * math.floor((d + 1) * (x / 255))), rc))

            # if math.sqrt(rc[0] ** 2 + rc[1] ** 2 + rc[2] ** 2) < 10:
            #     rc = (0, 0, 0)

            res_image.putpixel((x, y), tuple(rc))

    print("complete.")
    return res_image


def nabla(z, cs) -> tuple[float, float]:
    # d = math.sqrt(z[0] ** 2 + z[1] ** 2)
    # k = 255 * math.cos(math.pi ** 3 * d) / d if d != 0 else 0

    # return (z[0] * k, z[1] * k)

    # f(x, y) = (x-y)/(2.4cos((x+y)/(500pi))), freq ~ 1/500pi, ampl ~ 2.4

    freq_r = 500
    ampl_r = 2.8

    r = (z[0] + z[1]) / (freq_r*math.pi)

    k = math.sin(r) / (ampl_r * freq_r * math.pi * math.cos(r) ** 2)

    z_p = [
        (z[0] - z[1]) * k + 1/(ampl_r * math.cos(r)),
        (z[0] - z[1]) * k - 1/(ampl_r * math.cos(r))
    ]

    z_p[0] *= -1
    z_p[1] *= -1

    return z_p

    # z_p = (z[0] * k, z[1] * k)

    # if z_p[0] ** 2 + z_p[1] ** 2 < 100:
    #     return (0, 0)
    # else:
    #     return z_p

    # d = math.sqrt(z[0] ** 2 + z[1] ** 2)
    # k = -25*math.sin(d/(2*math.pi))/(math.pi*d) / d if d != 0 else 0

    # return (z[0] * k, z[1] * k)

    # d_sq = lambda c: (z[0] - c[0]) ** 2 + (z[1] - c[1]) ** 2
    # d = lambda c: math.sqrt((z[0] - c[0]) ** 2 + (z[1] - c[1]) ** 2)
    # dir = lambda c: [(z[0] - c[0]) / r, (z[1] - c[1]) / r]

    # res = [0, 0]

    # nearest = min(cs, key=d_sq)

    # for c in cs:
    #     r2 = d(c)

    #     if r2 == 0:
    #         continue

    #     r = r2 ** 0.5

    #     res[0] += dir(c)[0]
    #     res[1] += dir(c)[1]
    
    # if d((0, 0)) < 100:
    #     return nearest
    
    # return res


def get_rc0(grad):
    if math.sqrt(grad[0] ** 2 + grad[1] ** 2) == 0:
        return (0, 0, 0)

    angle = math.atan2(grad[1], grad[0])
    # if grad[0] < 0:
    #     angle += math.pi
    
    third = 2 * math.pi / 3

    component_factor = (angle // third) % 3

    C_alpha, C_beta = [0, 0, 0], [0, 0, 0]

    e1, e2, e3 = \
        [130, 209, 115], \
        [219, 80, 74], \
        [76, 44, 105]
    
    e1 = list(map(lambda x: x / 255, e1))
    e2 = list(map(lambda x: x / 255, e2))
    e3 = list(map(lambda x: x / 255, e3))

    if component_factor == 0:
        C_alpha = e1 # R
        C_beta = e2 # G
    elif component_factor == 1:
        C_alpha = e2 # G
        C_beta = e3 # B
    else:
        C_alpha = e3 # B
        C_beta = e1 # R
    
    norm_angle = angle % third
    alpha = (third - norm_angle) / third
    beta = 1 - alpha

    big_measure = 255 * math.sqrt(grad[0] ** 2 + grad[1] ** 2)

    C_alpha = list(map(lambda x: x * alpha * big_measure if x else 0, C_alpha))
    C_beta = list(map(lambda x: x * beta * big_measure if x else 0, C_beta))

    return list(map(lambda x: x[0] + x[1], zip(C_alpha, C_beta)))


def save_image(image: Image, image_name: str) -> None:
    i = 0

    name = image_name.split('.')[0]

    if not os.path.exists(name):
        os.mkdir(name)
    save_path = lambda i: f"{name}\\gen_{i}.png"

    while os.path.exists(save_path(i)):
        i += 1
    
    image.save(save_path(i))


def apply(args: Arguments) -> Image:
    centers = []

    if args.get_value('-c'):
        centers = list(map(lambda pair: eval(pair), args.get_value('-c')))
    
    if args.get_value('-p'):
        polynom = eval(args.get_value('-p')[0])
        part = 2 * math.pi / polynom[0]

        for i in range(polynom[0]):
            centers.append((
                polynom[1] * math.cos(part * i),
                polynom[1] * math.sin(part * i)
            ))

    print("centers:")
    for center in centers:
        print(center)
    print()

    hb = eval(args.get_value('-hb')[0])
    vb = eval(args.get_value('-vb')[0])

    print(f"OX : {hb[0]} <-> {hb[1]}")
    print(f"OY : {vb[0]} <-> {vb[1]}")

    size = eval(args.get_value('-s')[0])

    if args.get_value('--gradient'):
        return draw_grad(centers, hb, vb, size)
    else:
        return draw_calc(centers, hb, vb, size)


if __name__ == '__main__':
    args = Arguments()
    args.parse(sys.argv[1:])

    args.add_association(('-g', '--gradient'))

    # centers
    args.add_association(('-c', '--centers'))
    args.add_association(('-p', '--polygon'))

    args.add_association(('-hb', '--horizontal-borders'))
    args.add_association(('-vb', '--vertical-borders'))

    args.add_association(('-s', '--canvas-size'))

    args.add_association(('-o', '--output'))

    output_name = args.get_value('-o')
    if output_name:
        output_name = output_name[0]
        image = apply(args)
        if image != None:
            save_image(image, output_name)
