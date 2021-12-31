from PIL import Image as i
import numpy as np
from threading import Thread as thr

path = 'small'
t_number = 4

new_width = 640
size = 200
wt = i.open('watermark.png')


def resize(im, new_width):
    new_size = (new_width, int(im.size[1] * new_width / im.size[0]))
    new_im = im.resize(new_size)


def thumb(im, size):
    w, h = im.size
    new_size = (size, int(h * size / w)) if h > w else (int(w * size / h), size)
    new_im = im.resize(new_size).crop((0, 0, size, size))


def water(im, wt):
    nem_im = im.copy()
    nem_im.paste(wt, mask=wt)


def full_transform(image_list, new_width, size, bwt):
    for im in image_list:
        resize(im, new_width)
        thumb(im, size)
        water(im, wt)


def main():
    # Serial #
    with open(f'{path}/img-process-list.txt') as ipl:
        all_images = [i.open(f'{path}/{im.strip()}') for im in ipl]
    grouped_images = np.array_split(all_images, t_number)

    # Parallel #
    thread_list = [thr(target=full_transform, args=(images, new_width, size, wt)) for images in grouped_images]
    for th in thread_list:
        th.start()
    (th.join() for th in thread_list)
