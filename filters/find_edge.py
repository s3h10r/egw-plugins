#!/usr/bin/env python
#coding=utf-8
import math
from PIL import Image
from .adjustment import invert
from .utils import Matrix33
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "find_edge"
description = "a filter."
kwargs = {'image' : '<instance of PIL Image>',
          'angle' : 60, }
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

def run(image, angle = 60):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    return _find_edge(image, angle = 60)

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


def _find_edge(img, angle = 60):
    '''
    @效果：查找边缘
    @param img: instance of Image
    @param angle: 角度，大小[0, 360]
    @return: instance of Image
    '''

    radian = angle * 2.0 * math.pi / 360.0

    pi4 = math.pi / 4.0

    matrix33 = [
        [int(math.cos(radian + pi4) * 256),
         int(math.cos(radian + 2.0 * pi4) * 256),
         int(math.cos(radian + 3.0 * pi4) * 256)],
        [int(math.cos(radian) * 256),
         0,
         int(math.cos(radian + 4.0 * pi4) * 256)],
        [int(math.cos(radian - pi4) * 256),
         int(math.cos(radian - 2.0 * pi4) * 256),
         int(math.cos(radian - 3.0 * pi4) * 256)]
        ]

    m = Matrix33(matrix33, scale=256)

    img = m.convolute(img) # 对图像进行3*3卷积转换

    return invert(img) # 对图像进行负像处理
