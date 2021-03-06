from PIL import Image as i
import numpy as np
from threading import Thread as thr
from os.path import exists
from os import mkdir

# ssh ist189792@sigma

path = 'small'
t_number = 4

new_width = 640
size = 200
watermark = i.open('watermark.png')


def outpath(im, subfolder):
    directory, filename = im.filename.split('/')
    return f'{directory}/{subfolder}/{filename}'


def resize(im, new_width):
    if exists(new_path := outpath(im, 'Resized')): return
    new_size = (new_width, int(im.size[1] * new_width / im.size[0]))
    new_im = im.resize(new_size)
    new_im.save(new_path)


def thumb(im, size):
    if exists(new_path := outpath(im, 'Thumbnails')): return
    w, h = im.size
    new_size = (size, int(h * size / w)) if h > w else (int(w * size / h), size)
    new_im = im.resize(new_size).crop((0, 0, size, size))
    new_im.save(new_path)


def water(im, watermark):
    if exists(new_path := outpath(im, 'Watermarks')): return
    new_im = im.copy()
    new_im.paste(watermark, mask=watermark)
    new_im.save(new_path)


def resize_c(image_list, new_width):
    #inicio thread
    for im in image_list:
        resize(im, new_width)
    #fim thread


def thumb_c(image_list, size):
    #inicio thread
    for im in image_list:
        thumb(im, size)
    #fim thread


def water_c(image_list, watermark):
    #inicio thread
    for im in image_list:
        water(im, watermark)
    #fim thread


def main(dir, n):
    #epoch

    # Serial #
    with open(f'{path}/img-process-list.txt') as ipl:
        all_images = [i.open(f'{path}/{im.strip()}') for im in ipl]
    grouped_images = np.array_split(all_images, n)

    not exists(dir := f'{path}/Resized') and mkdir(dir)
    not exists(dir := f'{path}/Thumbnails') and mkdir(dir)
    not exists(dir := f'{path}/Watermarks') and mkdir(dir)

    # Parallel #
    # Resizing
    thread_list = [thr(target=resize, args=(images, new_width)) for images in grouped_images]

    #inicio
    [th.start() for th in thread_list]
    [th.join() for th in thread_list]
    #fim

    # Thumb
    thread_list = [thr(target=thumb, args=(images, size)) for images in grouped_images]

    # inicio
    [th.start() for th in thread_list]
    [th.join() for th in thread_list]
    # fim

    # water
    thread_list = [thr(target=water, args=(images, watermark)) for images in grouped_images]

    # inicio
    [th.start() for th in thread_list]
    [th.join() for th in thread_list]
    # fim

    #end_epoch

    #save estatistica : lista/lista de listas -> Save

if __name__ == '__main__':
    main(path, t_number)
