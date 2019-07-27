#!/usr/bin/env python
#coding=utf-8
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "invert"
description = "a simple filter which inverts each pixel of the image"
kwargs = { 'image' : '<instance of PIL Image>', }
args = None
author = "Sven Hessenmüller <sven.hessenmueller@gmail.com>"
version = "0.1.0"

def run(**kwargs):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    return _invert_image(**kwargs)

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
def _invert_image(image = None):
    return image.point(lambda x: 255 - x)
