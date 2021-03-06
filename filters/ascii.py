#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import glob
from io import StringIO
import logging
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
from einguteswerkzeug.helpers.gfx import get_exif, scale_image_to_square, scale_image, scale_square_image, trim
from einguteswerkzeug.plugins import EGWPluginFilter

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

fmeta = {
    "name" : "ascii",
    "version" : "0.2.1",
    "description" : "this filter converts an image into ascii-art",
    "author" : "diverse"
}

class ASCIIArt(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'color' : (0,0,0), }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        """
        implement this in the subclass or overwrite `.run()`` in it
        """
        img = self.kwargs['image']
        img_as_ascii = _convert_image_to_ascii(img)
        img = _convert_ascii_to_image(img_as_ascii, self.kwargs['color'])
        return img


filter = ASCIIArt()
assert isinstance(filter,EGWPluginFilter)


# --- different variants of image to ascii & reverse found on the internet
#     please see source & copyright infos in the docstrings
def _image_to_ascii(image, buckets=25):
    """
    replaces each pixel with a ascii-character which's intensity is similar
    source: https://github.com/s3h10r/asciify
    """
    ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
    ASCII_CHARS = ASCII_CHARS[::-1] #?
    img = image.convert('L') # turn into grayscale
    pixels = list(image.getdata())
    ascii_pixels = [ASCII_CHARS[(pixel_value[0])//buckets] for pixel_value in pixels]
    ascii_pixels = ''.join(ascii_pixels)
    w_out = img.size[0]
    len_pixels = len(ascii_pixels)
    img_as_ascii = [ascii_pixels[index:index+w_out] for index in range(0, len_pixels, w_out)]
    return '\n'.join(img_as_ascii)

def _image_to_ascii2(image):
    """
    # ASCII Art Generator (Image to ASCII Art Converter)
    # FB - 20160925
    source : http://code.activestate.com/recipes/580702-image-to-ascii-art-converter/
    """
    font = ImageFont.load_default() # load default bitmap monospaced font
    (chrx, chry) = font.getsize(chr(32))
    # calculate weights of ASCII chars
    weights = []
    for i in range(32, 127):
        chrImage = font.getmask(chr(i))
        ctr = 0
        for y in range(chry):
            for x in range(chrx):
                if chrImage.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chrx * chry))
    (imgx, imgy) = image.size
    imgx = int(imgx / chrx)
    imgy = int(imgy / chry)
    # NEAREST/BILINEAR/BICUBIC/ANTIALIAS
    image = image.resize((imgx, imgy), Image.BICUBIC)
    image = image.convert("L") # convert to grayscale
    pixels = image.load()
    img_as_ascii = StringIO()
    for y in range(imgy):
        for x in range(imgx):
            w = float(pixels[x, y]) / 255
            # find closest weight match
            wf = -1.0; k = -1
            for i in range(len(weights)):
                if abs(weights[i] - w) <= abs(wf - w):
                    wf = weights[i]; k = i
            img_as_ascii.write(chr(k + 32))
        img_as_ascii.write("\n")
    return img_as_ascii.getvalue()

def _convert_image_to_ascii(image):
    return _image_to_ascii2(image)

PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"
large_font = 12  # get better resolution with larger size
def _convert_ascii_to_img(ascii_str, font_path='fonts/Menlo-Regular.ttf', color=(0,0,225)):
    """
    Copyright (c) 2018 Jianzhu Guo (MIT License)
    original source of this [ImageToAscii](https://github.com/cleardusk/ImageToAscii/blob/master/img_to_ascii.py)

    Convert text file to a grayscale image with black characters on a white background.

    arguments:
    ascii_str - string of ascii format
    font_path - path to a font file (for example impact.ttf)
    """
    mode = 'RGBA'
    #mode = grayscale = 'L'
    ascii_str = ascii_str.replace('\r\n', '\n')  # for windows
    lines = ascii_str.rstrip().split('\n')

    # choose a font (you can see more detail in my library on github)
    # font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # _convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    if mode != 'L':
        image = Image.new(mode, (width, height), color=(255,255,255))
    else:
        image = Image.new(mode, (width, height), color=PIXEL_OFF)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        if mode != 'L':
            PIXEL_ON = color
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing

    # return image
    # crop the text
    if mode == 'L':
        c_box = ImageOps.invert(image).getbbox()
    else:
        return trim(image)
    image = image.crop(c_box)
    return image

def _convert_ascii_to_image(image_as_ascii, color = (0,0,0)):
    ascii_str = image_as_ascii
    image = _convert_ascii_to_img(ascii_str, color=color)
    return image
# ---

def _ascii_to_console(img_as_ascii = None):
    print(img_as_ascii)
