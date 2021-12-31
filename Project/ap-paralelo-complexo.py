from PIL import Image as i
import numpy as np
from threading import Thread as thr
from os.path import exists
from os import mkdir

path = 'small'
t_number = 4

new_width = 640
size = 200
watermark = i.open('watermark.png')


def outpath(im, subfolder):
    directory, filename = im.filename.split('/')
    return f'{directory}/{subfolder}/{filename}'


def resize(image_list, new_width):
    for im in image_list:
        if exists(new_path := outpath(im, 'Resized')): continue
        new_size = (new_width, int(im.size[1] * new_width / im.size[0]))
        new_im = im.resize(new_size)
        new_im.save(new_path)


def thumb(image_list, size):
    for im in image_list:
        if exists(new_path := outpath(im, 'Thumbnails')): continue
        w, h = im.size
        new_size = (size, int(h * size / w)) if h > w else (int(w * size / h), size)
        new_im = im.resize(new_size).crop((0, 0, size, size))
        new_im.save(new_path)


def water(image_list, watermark):
    for im in image_list:
        if exists(new_path := outpath(im, 'Watermarks')): continue
        new_im = im.copy()
        new_im.paste(watermark, mask=watermark)
        new_im.save(new_path)


def main():
    # Serial #
    with open(f'{path}/img-process-list.txt') as ipl:
        all_images = [i.open(f'{path}/{im.strip()}') for im in ipl]
    grouped_images = np.array_split(all_images, t_number)

    not exists(dir := f'{path}/Resized') and mkdir(dir)
    not exists(dir := f'{path}/Thumbnails') and mkdir(dir)
    not exists(dir := f'{path}/Watermarks') and mkdir(dir)

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
    thread_list = [thr(target=water, args=(images, watermark)) for images in grouped_images]
    for th in thread_list:
        th.start()
    (th.join() for th in thread_list)
