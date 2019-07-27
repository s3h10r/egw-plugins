#!/usr/bin/env python3
#coding=utf-8

# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "mosaic"
description = "a filter which pixelates the picture"
kwargs = { 'image' : '<instance of PIL Image>', 'block_size' : 32, } # plugin specific arguments (if any)
args = None
author = "Chine, 2011, https://github.com/Tinker-S/SomeImageFilterWithPython"
version = "0.2.0"

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(image, block_size):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    return _mosaic(image, block_size)

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

from PIL import Image

def _mosaic(img, block_size = 32):
    '''
    @param img: instance of Image
    @param block_size: [1, N]
    @return: instance of Image
    '''

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    width, height = img.size
    pix = img.load()

    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()

    for w in range(0, width, block_size):
        for h in range(0, height, block_size):
            r_sum, g_sum, b_sum = 0, 0, 0
            size = block_size ** 2

            for i in range(w, min(w+block_size, width)):
                for j in range(h, min(h+block_size, height)):
                    r_sum += pix[i, j][0]
                    g_sum += pix[i, j][1]
                    b_sum += pix[i, j][2]

            r_ave = int(r_sum / size)
            g_ave = int(g_sum / size)
            b_ave = int(b_sum / size)

            for i in range(w, min(w+block_size, width)):
                for j in range(h, min(h+block_size, height)):
                    dst_pix[i, j] = r_ave, g_ave, b_ave, pix[w, h][3]

    return dst_img

if __name__ == "__main__":
    print(get_plugin_doc)
    #start = time.time()
    #end = time.time()
    #print('It all spends %f seconds time' % (end-start))
