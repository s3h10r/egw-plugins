#!/usr/bin/env python
#coding=utf-8

# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import random
import string
import sys

from PIL import Image, ImageDraw

name = "puzzle"
description = "a filter about guess what"
author = ""
version = "0.0.2"
__version__ = version

kwargs = {'image' : '<instance of PIL Image>', 'seed' : random.randrange(sys.maxsize)}

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
    return _do_puzzle(**kwargs)
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

def _do_puzzle(image = None, seed = None):
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    log.info("seed: {}".format(seed))
    im = image
    width, height = im.size
    width = int( ((width + 99) / 100) * 100 )
    height = int( ((int(height + 99) / 100)) * 100 )
    im = im.crop((0, 0, width, height))
    im2 = Image.new("RGB", (width, height), "black")
    blocks = []
    for x in range(int(width / 100)):
        for y in range(int(height / 100)):
            blocks.append(im.crop((x * 100, y * 100, (x + 1) * 100, (y + 1) * 100)))
    random.shuffle(blocks)
    for x in range(int(width / 100)):
        for y in range(int(height / 100)):
            im2.paste(blocks.pop().rotate(90 * random.randint(0,3)), (x * 100, y * 100))
    return im2

if __name__ == '__main__':
    print(get_plugin_doc())
