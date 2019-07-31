#!/usr/bin/env python
#coding=utf-8

# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import random
import string
from einguteswerkzeug.helpers import get_resource_file

name = "sprites"
description = "generates random sprites - space invaders style. :) https://medium.freecodecamp.org/how-to-create-generative-art-in-less-than-100-lines-of-code-d37f379859f"
kwargs = {'size' : random.randrange(3,99,2), # must be an odd integer
          #'invaders' : random.randint(1,150), # nr invaders per row
          'invaders' : random.randint(1,60), # nr invaders per row
          'img_size'  : 800,
          'file_out' : None,
          }
args=None
author = "Eric Davidson"
version = '0.2.0'
__version__ = version

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(size = 13, invaders = 8, img_size = 600, file_out = None):
    """
    this is the wrapper around the functionality of the plugin.
    """
    return _sprites_main(size = size, invaders = invaders, img_size = img_size, file_out = file_out), "generator %s v%s" % (name, __version__)

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
from .sprites import main as _sprites_main
