#!/usr/bin/env python
#coding=utf-8
import math
from PIL import Image
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "glowing_edge"
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
    return _glowing_edge(image)

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


def _glowing_edge(img):
    '''
    @效果：照亮边缘
    @param img: instance of Image
    @return: instance of Image
    '''

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    width, height = img.size
    pix = img.load()

    for w in range(width-1):
        for h in range(height-1):
            bottom = pix[w, h+1] # 下方像素点
            right = pix[w+1, h] # 右方像素点
            current = pix[w, h] # 当前像素点

            # 对r, g, b三个分量进行如下计算
            # 以r分量为例：int(2 * math.sqrt((r[current]-r[bottom])^2 + r[current]-r[right])^2))
            pixel = [int(math.sqrt((item[0] - item[1]) ** 2 + (item[0] - item[2]) ** 2) * 2)
                     for item in list(zip(current, bottom, right))[:3]]
            pixel.append(current[3])

            pix[w, h] = tuple([min(max(0, i), 255) for i in pixel]) # 限制各分量值介于[0, 255]

    return img
