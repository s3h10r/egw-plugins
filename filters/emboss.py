#!/usr/bin/env python
#coding=utf-8
from PIL import Image
from .utils import Matrix33
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "emboss"
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
    return _emboss(image)

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

def _emboss(img):
    '''
    @效果：浮雕
    @param img: instance of Image
    @return: instance of Image

    @不推荐使用，PIL已经内置浮雕的滤镜处理
    '''

    # 要进行卷积转换的3×3矩阵
    matrix33 = [[-1, 0, -1],
                [0, 4, 0],
                [-1, 0, -1]]
    m = Matrix33(matrix33, offset=127)
    return m.convolute(img) # 进行卷积转换

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])

    if len(sys.argv) > 1:
        path = sys.argv[1]

    start = time.time()

    img = Image.open(path)
    img = emboss(img)
    img.save(os.path.splitext(path)[0]+'.emboss.png', 'PNG')

    end = time.time()
    print(('It all spends %f seconds time' % (end-start)))

'''
    from PIL import ImageFilter

    start = time.time()

    img = Image.open(path)
    img = img.filter(ImageFilter.EMBOSS)
    img.save(os.path.splitext(path)[0]+'.emboss2.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)
'''
