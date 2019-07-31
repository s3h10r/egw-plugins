#!/usr/bin/env python
#coding=utf-8

# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import random
import string
import subprocess
from cowpy import cow
from PIL import  Image, ImageDraw, ImageFont
from einguteswerkzeug.helpers import get_resource_file
from einguteswerkzeug.helpers.gfx import scale_image_to_square
name = "cowsay"
description = "aphorisms, thoughts, affirmations"
kwargs = {'message' : None,
          'messages' : "messages.json", # quotes or alike
          'cowfiles' : "/usr/share/cowsay/cows", #templates
          'cowsay_bin' : "/usr/games/cowsay",
          }
args=None
author = "Sven Hessenmüller"
version = '0.1.2'
__version__ = version

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(message, messages, cowfiles, cowsay_bin):
    """
    this is the wrapper around the functionality of the plugin.
    """
    return _somework(message=message, messages=messages, cowfiles=cowfiles, cowsay_bin=cowsay_bin) , "generator %s v%s" % (name, __version__)

# --- END all einguteswerkzeug-plugins (generators, filters) must implement this

def get_plugin_doc(format='text'):
    """
    """
    if format not in ('txt', 'text', 'plaintext'):
        raise Exception("Sorry. format %s not available. Valid options are ['text']" % format)
    tpl_doc = string.Template("""
    filters.$name - $description
    kwargs  : $kwargs
    args    : $args
    author  : $author
    version : __version__
    """)
    return tpl_doc.substitute({
        'name' : name,
        'description' : description,
        'kwargs' : kwargs,
        'args'    : args,
        'author'  : author,
        'version' : __version__,
        })

if __name__ == '__main__':
    print(get_plugin_doc())

# === END einguteswerkzeug plugin-interface

# --- .. here comes the plugin-specific part to get some work done...

def _somework(message=None, messages=None, cowfiles=None, cowsay_bin = None, color = (0,0,255)):
    if message :
        msg = cow.milk_random_cow(message)
    else:
        msg = cow.milk_random_cow("carpe diem dude!")
    log.debug(msg)
    img = _convert_msg_to_image(msg, color)

    return img

def _convert_msg_to_image(message, color, font_path='fonts/Menlo-Regular.ttf'):
    mode = 'RGBA'
    lines = message.split('\n')
    try:
        font = ImageFont.truetype(font_path, size=12)
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
    image = Image.new(mode, (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(image)

    vertical_position = 10
    horizontal_position = 45
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=color, font=font)
        vertical_position += line_spacing
    image = scale_image_to_square(image)
    return image
