#!/usr/bin/env python
#coding=utf-8
from PIL import Image
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "molten"
description = "a filter."
kwargs = {'image' : '<instance of PIL Image>', }
args = None
author = "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
version = "0.1.8"

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(image):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    return _molten(image)

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


def _molten(img):
    '''
    @效果：熔铸
    @param img: instance of Image
    @return: instance of Image
    '''

    if img.mode != "RGB":
        img.convert("RGB")

    width, height = img.size
    pix = img.load()

    for w in range(width):
        for h in range(height):
            r, g, b = pix[w, h]

            pix[w, h] = min(255, int(abs(r * 128 / (g + b + 1)))), \
                        min(255, int(abs(g * 128 / (b + r + 1)))), \
                        min(255, int(abs(b * 128 / (r + g + 1))))

    return img
