#!/usr/bin/env python
#coding=utf-8
import random
from PIL import Image
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "diffuse"
description = "a filter."
kwargs = {'image' : '<instance of PIL Image>',
          'diffuse' : random.randint(1,32), }
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

def run(image, degree = 32):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    return _diffuse(image, degree)

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

def _diffuse(img, degree = 32):
    '''
    @效果：扩散
    @param img: instance of Image
    @param degree: 扩散范围，大小[1, 32]
    @return: instance of Image
    '''

    degree = min(max(1, degree), 32)

    width, height = img.size

    dst_img = Image.new(img.mode, (width, height))

    pix = img.load()
    dst_pix = dst_img.load()

    for w in range(width):
        for h in range(height):
            # 随机获取当前像素周围一随机点
            x = w + random.randint(-degree, degree)
            y = h + random.randint(-degree, degree)

            # 限制范围
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)

            dst_pix[w, h] = pix[x, y]

    return dst_img
