from PIL import Image as i
import numpy as np
from threading import Thread as thr

path = 'small'
t_number = 4

new_width = 640
size = 200
wt = i.open('watermark.png')


def resize(image_list, new_width):
    for im in image_list:
        new_size = (new_width, int(im.size[1] * new_width / im.size[0]))
        new_im = im.resize(new_size)


def thumb(image_list, size):
    for im in image_list:
        w, h = im.size
        new_size = (size, int(h * size / w)) if h > w else (int(w * size / h), size)
        new_im = im.resize(new_size).crop((0, 0, size, size))


def water(image_list, wt):
    for im in image_list:
        nem_im = im.copy()
        nem_im.paste(wt, mask=wt)


def main():
    # Serial #
    with open(f'{path}/img-process-list.txt') as ipl:
        all_images = [i.open(f'{path}/{im.strip()}') for im in ipl]
    grouped_images = np.array_split(all_images, t_number)

    # Parallel #
    # Resizing
    thread_list = [thr(target=resize, args=(images, new_width)) for images in grouped_images]
    for th in thread_list:
        th.start()
    (th.join() for th in thread_list)

    # Thumb
    thread_list = [thr(target=thumb, args=(images, size)) for images in grouped_images]
    for th in thread_list:
        th.start()
    (th.join() for th in thread_list)

    # water
    thread_list = [thr(target=water, args=(images, wt)) for images in grouped_images]
    for th in thread_list:
        th.start()
    (th.join() for th in thread_list)
