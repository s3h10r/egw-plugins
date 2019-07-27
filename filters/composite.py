#!/usr/bin/env python
#coding=utf-8
"""
based on
https://stackoverflow.com/questions/29106702/blend-overlapping-images-in-python
https://stackoverflow.com/questions/3374878/with-the-python-imaging-library-pil-how-does-one-compose-an-image-with-an-alp
"""
from PIL import Image
from einguteswerkzeug.helpers.gfx import crop_image_to_square, scale_square_image
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "composite"
description = "blend N overlapping images"
kwargs = {'image' : 'list[<instance of PIL Image>, ...]',
          'alpha' : 0.5,
          'use_sigmoid' : False
         }
args = None
author = "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
version = "0.1.2"

def run(**kwargs):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    #call the plugin-specific function(s) here
    if not kwargs :
        #use default values if no args given
        return _do_some_work()
    else:
        return _do_some_work(**kwargs)

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
def _do_some_work(image,alpha=0.5,use_sigmoid=False):
    if use_sigmoid:
        log.critical("filter-plugin '%s' arg 'use_sigmoid' is not implemented yet. does nothing." % name)

    result = crop_image_to_square(image[0])
    for img in image:
        # make sure images have equal size (take the first one as reference to risize if not)
        if img.size[0] != result.size[0] or img.size[1] != result.size[1]:
            img = crop_image_to_square(img)
            img = scale_square_image(img, size = result.size[0])
        # RGBA-mode only
        #img.put_alpha(alpha) # make sure image has an alpha channel
        #result = Image.alpha_composite(result, img)
        # without RGBA:
        result = Image.blend(result, img, alpha=alpha)
    return result
