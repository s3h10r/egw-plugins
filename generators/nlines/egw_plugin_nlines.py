#!/usr/bin/env python
#coding=utf-8
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import json
import math
import random
import string
import sys

from PIL import Image, ImageDraw

name = "nlines"
description = "a generator plotting n lines shaped by randomness"
kwargs = {  'nr_lines' : random.randint(3,800/20), 'thickness' : random.randint(1, 800/100),
            'x_step' : random.randint(1,800/8), 'img_mode' : 'RGBA',
            'color' : (random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(200,255)),
            'bg_color' : None, # if None then the generator chooses the complementary color to color for this
            'draw_baseline' : False,
            'seed' : random.randrange(sys.maxsize),
            'size' : 800,
          }
author = "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
version = "0.1.2"
__version__ = version

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(**kwargs):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    meta = None
    return _generate_nlines(**kwargs), meta
# --- END all einguteswerkzeug-plugins (generators, filters) must implement this

def get_plugin_doc(format='text'):
    """
    """
    if format not in ('txt', 'text', 'plaintext'):
        raise Exception("Sorry. format %s not available. Valid options are ['text']" % format)
    tpl_doc = string.Template("""
    generator.$name - $description
    kwargs  : $kwargs
    author  : $author
    version : $version
    """)
    return tpl_doc.substitute({
        'name' : name,
        'description' : description,
        'kwargs' : kwargs,
        'author'  : author,
        'version' : __version__,
        })

# === END einguteswerkzeug plugin-interface

# --- .. here comes the plugin-specific part to get some work done...

# --- find complement color helpers
# https://stackoverflow.com/questions/40233986/python-is-there-a-function-or-formula-to-find-the-complementary-colour-of-a-rgb

# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))
# --- END find complement color

# --- producing some random values in a given range
def _random_value(x = None, min=0, max=10):
    """
    (not very eye pleasing ;)
    returns a random int between min and max
    """
    return random.randint(min,max)

def _custom_random(x = None, min=0, max=10, power=5):
    """
    isn't quite as random as random (a bit more pleasing to the eye than random)
    returns a random in between min and max
    """
    res = 1 - (random.random()**power)
    #btw. if we would raises the random number to 2 (square) the value tend to be more to 0
    #     if we would raise to the power of half the number would turn mor towards 1
    res = min + ((max - min)/ 1) * res
    return res

def _sine_stuff(x,min,max):
    res = min + ((max - min)/ 1) * math.sin(x)
    return abs(res)
# ---

# here we go
def _generate_nlines(nr_lines = 10, thickness = 3, x_step = 10, img_mode = 'RGBA', color = (0,0,0,255), bg_color = None, draw_baseline = True, seed = None, size=800):
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    complement_color = complement(color[0], color[1], color[2])
    if img_mode == 'RGBA':
        complement_color = (complement_color[0],complement_color[1],complement_color[2],255)
    if not bg_color:
        log.debug("setting bg_color to complement of {}: {}".format(color,complement_color))
        bg_color = complement_color
    img = Image.new(img_mode, (size,size), bg_color)
    margin = int(size * 0.10)
    max_line_height = int ((size - margin*2)/ nr_lines)
    max_line_length = int(size - margin*2)
    log.debug("nr_lines: {} x_step: {} thickness: {} margin: {}".format(nr_lines, x_step, thickness, margin))
    log.debug("max_line_height: {} max_line_length: {}".format(max_line_height, max_line_length,))
    if max_line_length % x_step != 0:
        while max_line_length % x_step != 0:
            x_step -= 1
        log.info("x_step autocorrected to: {}".format(x_step))
    draw = ImageDraw.Draw(img)
    xf = 0 + margin         # from
    yf = margin + max_line_height
    xt = size - margin      # to
    yt = yf
    for i in range(nr_lines):
        if draw_baseline:
            draw.line((xf,yf, xt, yt), fill=color, width=thickness)
        last_y = yf
        last_x = xf
        for x in range(int(margin), int(margin) + max_line_length + 1, x_step):
            #print(x)
            if i % 2 == 0:
                #print(x, x_step, max_line_length)
                new_y = yf - max_line_height * 0.8 + _custom_random(x, min=0, max=max_line_height * 0.8, power=4)
                new_x = x
                draw.line((last_x, last_y, new_x, new_y ), fill=color, width=thickness)
            else:
                new_y = yf - max_line_height * 0.3 + _custom_random(x, min=0, max=max_line_height * 0.3, power=5)
                new_x = x
                draw.line((last_x, last_y, new_x, new_y ), fill=color, width=thickness)
            last_x = new_x
            last_y = new_y
        yf += max_line_height
        yt = yf
    return img

if __name__ == '__main__':
    print(get_plugin_doc())
    img = _generate_nlines(**kwargs)
    if len(sys.argv) > 1:
        fout = sys.argv[1]
        img.save(fout)
    else:
        print("usage (selftest): %s <file_out.jpg>" % __file__)
