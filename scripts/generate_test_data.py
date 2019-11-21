import json
from random import randint, choice
import string
import os
from glob import glob
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
import numpy as np


def random_font():
    fontname = choice(list(glob('fonts/*.ttf')))
    font = ImageFont.truetype(fontname, size=randint(24, 32))
    return font


def rand_pad():
    return randint(5, 35), randint(5, 35), randint(0, 3), randint(10, 13)


def random_string(length):
    letters = list(string.ascii_uppercase) + list(string.ascii_lowercase) + list(string.digits) + [' ', '-', '.', ':', '?', '!', '<', '>', '#', '@', '(', ')', '$', '%', '&']
    return (''.join(choice(letters) for _ in range(length))).strip()


def random_background(height, width):
    background_image = choice(list(glob('images/*.jpg')))
    original = Image.open(background_image)
    L = original.convert('L')
    original = Image.merge('RGB', (L, L, L))
    left = randint(0, original.size[0] - height)
    top = randint(0, original.size[1] - width)
    right = left + height
    bottom = top + width
    return original.crop((left, top, right, bottom))


def generate_image(txt='Hello world!') -> Tuple[np.array, str, list]:
    font = random_font()
    txt_width, txt_height = font.getsize(txt)
    left_pad, right_pad, top_pad, bottom_pad = rand_pad()

    print(txt_height)
    print(left_pad, right_pad, top_pad, bottom_pad)
    height = left_pad + txt_width + right_pad
    width = top_pad + txt_height + bottom_pad
    img = random_background(height, width)
    stroke_sat = int(np.array(img).mean())
    sat = int((stroke_sat + 127) % 255)
    canvas = ImageDraw.Draw(img)
    canvas.text((left_pad, top_pad), txt, fill=(sat, sat, sat), font=font, stroke_width=2, stroke_fill=(stroke_sat, stroke_sat, stroke_sat))
    metadata = []
    for idx, char in enumerate(txt):
        char_width, _ = font.getmask(char).size
        x_offset, _ = font.getmask(txt[:idx]).size
        metadata.append({'char': char.lower(), 'x': left_pad + x_offset, 'width': char_width})
    return img, txt.lower(), metadata


if __name__ == "__main__":

    if not os.path.exists('train/'):
        os.mkdir('train/')
    if not os.path.exists('test/'):
        os.mkdir('test/')

    # import matplotlib.pyplot as plt
    #
    # img, txt, meta = generate_image(random_string(randint(4, 20)))
    # print(txt)
    # imgplot = plt.imshow(img)
    # plt.show()
    #
    # os.exit(-1)

    for i in range(90000):
        img, txt, meta = generate_image(random_string(randint(4, 20)))
        img.save('train/%s.jpg' % txt)
        with open('train/%s.json' % txt, 'w') as f:
            json.dump(meta, f)

    for i in range(256):
        img, txt, meta = generate_image(random_string(randint(4, 20)))
        img.save('test/%s.jpg' % txt)
        with open('test/%s.json' % txt, 'w') as f:
            json.dump(meta, f)
