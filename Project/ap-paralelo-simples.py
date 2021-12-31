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


def resize(im, new_path, new_width):
    new_size = (new_width, int(im.size[1] * new_width / im.size[0]))
    new_im = im.resize(new_size)
    new_im.save(new_path)


def thumb(im, new_path, size):
    w, h = im.size
    new_size = (size, int(h * size / w)) if h > w else (int(w * size / h), size)
    new_im = im.resize(new_size).crop((0, 0, size, size))
    new_im.save(new_path)


def water(im, new_path, watermark):
    new_im = im.copy()
    new_im.paste(watermark, mask=watermark)
    new_im.save(new_path)


def full_transform(image_list, new_width, size, watermark):
    for im in image_list:
        if not exists(new_path := outpath(im, 'Resized')): resize(im, new_path, new_width)
        if not exists(new_path := outpath(im, 'Thumbnails')): thumb(im, new_path, size)
        if not exists(new_path := outpath(im, 'Watermarks')): water(im, new_path, watermark)


def main():
    # Serial #
    with open(f'{path}/img-process-list.txt') as ipl:
        all_images = [i.open(f'{path}/{im.strip()}') for im in ipl]
    grouped_images = np.array_split(all_images, t_number)

    not exists(dir := f'{path}/Resized') and mkdir(dir)
    not exists(dir := f'{path}/Thumbnails') and mkdir(dir)
    not exists(dir := f'{path}/Watermarks') and mkdir(dir)

    # Parallel #
    thread_list = [thr(target=full_transform, args=(images, new_width, size, watermark)) for images in grouped_images]
    for th in thread_list:
        th.start()
    (th.join() for th in thread_list)
