#!/usr/bin/env python
#coding=utf-8
# === einguteswerkzeug plugin-interface ===
# --- all einguteswerkzeug-plugins (generators, filters) must implement this
import logging
import string

name = "example"
description = "a template you can use to roll your own plugins"
kwargs = { 'arg1' : 'val1', 'arg2' : 'val2', } # plugin specific arguments (if any)
author = "optional author and copyright infos"
version = "0.2.0"
__version__ = version

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def run(**kwargs):
    """
    this is the interface/wrapper around the functionality of the plugin.
    """
    #call the plugin-specific function(s) here
    if not kwargs :
        #use default values if no args given
        return _somework()
    else:
        return _somework(**kwargs)

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
def _somework(arg1=None, arg2 = None):
    return ("Hello from Plugin dummy1. arg1=%s, arg2=%s " % (arg1,arg2))

if __name__ == '__main__':
    print(get_plugin_doc())
