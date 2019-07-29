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

name = "mondrian"
description = "a simple recursive generator inspired by the art of Piet Mondrian"
long_description = """
Piet Mondrian (March 7, 1872 – February 1, 1944) was a Dutch painter.
He is known to be one of the pioneers of 20th century abstract art. Piet Mondrain
created numerous famous paintings in the early half of the previous century
that consisted of a white background, prominent black horizontal and vertical
lines, and regions colored with red, yellow and blue.
"""
author = "adopted from http://nifty.stanford.edu/2018/stephenson-mondrian-art/"
version = "0.1.2"
__version__ = version

kwargs = {  'width' : 1200, 'height' : 1200,
            'split_low' : 120, 'split_penalty' : 1.5,
            # default: red, blue, yellow, white
            'colors' : [(255,0,0,255),(135,206,255,255), (255,255,0,255), (255,255,255,255)],
            'bg_color' : (255,255,255,255),
            'outline_color' : (0,0,0,255),
            'outline_width' : None,
            'img_mode' : "RGBA",
            'seed' : random.randrange(sys.maxsize),
          }

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
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
    _setup_globals()
    return _do_mondrian(**kwargs), meta
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

def _setup_globals():
    """
    check & setup globals
    """
    global kwargs
    if not kwargs['outline_width']:
        kwargs['outline_width'] = int(kwargs['height'] * 0.005)
        log.info("setoutline_width to {}".format(kwargs['outline_width'] ))

def _do_mondrian(**kwargs):
    seed = kwargs['seed']
    img_mode = kwargs['img_mode']
    w = kwargs['width']
    h = kwargs['height']
    bg_color = kwargs['bg_color']
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    log.info("seed: {}".format(seed))
    img = Image.new(img_mode, (w,h), bg_color)
    img = _mondrian(x = 0, y = 0, w = w, h = h, image = img)
    return img

def _get_random_color(colors):
  #i = random.randint(0,len(colors)-1)
  #color = colors[i]
  rv = random.random()
  if rv < 0.0833:
    return colors[0]
  elif rv < 0.1667:
    return colors[1]
  elif rv < 0.25:
    return colors[2]
  else:
    return colors[3]

def _split_both(x, y, w, h, image):
    """
    Split the region both vertically and horizontally
    """
    hsp = random.randrange(33, 68) / 100
    vsp = random.randrange(33, 68) / 100
    left_width = round(hsp * w)
    right_width = w - left_width
    top_height = round(vsp * h)
    bottom_height = h - top_height
    _mondrian(x, y, left_width, top_height, image = image)
    _mondrian(x + left_width, y, right_width, top_height, image = image)
    _mondrian(x, y + top_height, left_width, bottom_height, image = image)
    _mondrian(x + left_width, y + top_height, right_width, bottom_height, image = image)

def _split_h(x, y, w, h, image):
    """
    Split so that the regions are side by side
    """

    hsp = random.randrange(33, 68) / 100
    left_width = round(hsp * w)
    right_width = w - left_width
    _mondrian(x, y, left_width, h, image = image)
    _mondrian(x + left_width, y, right_width, h, image = image)

def _split_v(x, y, w, h, image):
    """
    Split so that one region is above the other
    """
    vsp = random.randrange(33, 68) / 100
    top_height = round(vsp * h)
    bottom_height = h - top_height
    _mondrian(x, y, w, top_height, image = image)
    _mondrian(x, y + top_height, w, bottom_height, image = image)

def _mondrian(x = 0, y = 0, w = 1024, h = 768, image = None):
    """
    Use recursion to draw "art" in a Mondrian style
    """
    WIDTH, HEIGHT = image.size
    SPLIT_LOW = kwargs['split_low']
    SPLIT_PENALTY = kwargs['split_penalty']
    COLORS = kwargs['colors']
    OUTLINE_COLOR = kwargs['outline_color']
    OUTLINE_WIDTH = kwargs['outline_width']

    # Splits based on the size of the region
    if w > WIDTH / 2 and h > HEIGHT / 2:
        _split_both(x, y, w, h, image)
    elif w > WIDTH / 2:
        _split_h(x, y, w, h, image)
    elif h > HEIGHT / 2:
        _split_v(x, y, w, h, image)
    else:
        # Splits based on random chance
        hsplit = random.randrange(SPLIT_LOW, max(round(SPLIT_PENALTY * w) + 1, \
                           SPLIT_LOW + 1))
        vsplit = random.randrange(SPLIT_LOW, max(round(SPLIT_PENALTY * h) + 1, \
                           SPLIT_LOW + 1))
        if hsplit < w and vsplit < h:
            _split_both(x, y, w, h, image)
        elif hsplit < w:
            _split_h(x, y, w, h, image)
        elif vsplit < h:
            _split_v(x, y, w, h, image)
        # No split -- fill the region with yellow, blue, red or white
        else:
            draw = ImageDraw.Draw(image)
            draw.rectangle([(x, y), (x + w, y + h)], fill = _get_random_color(COLORS),outline=OUTLINE_COLOR, width = OUTLINE_WIDTH)
    return image

if __name__ == '__main__':
    print(get_plugin_doc())
    img,meat = run(**kwargs)
    if len(sys.argv) > 1:
        fout = sys.argv[1]
        img.save(fout)
    else:
        print("usage (selftest): %s <file_out.jpg>" % __file__)
