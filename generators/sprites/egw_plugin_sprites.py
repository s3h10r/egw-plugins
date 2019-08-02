#!/usr/bin/env python3
#coding=utf-8
import logging
import random
import string
import sys
from PIL import Image, ImageDraw
from einguteswerkzeug.helpers import get_resource_file
from einguteswerkzeug.plugins import EGWPluginGenerator

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

meta = {
    "name" : "sprites",
    "version" : "0.2.1",
    "description" : "generates random sprites - space invaders style. :) https://medium.freecodecamp.org/how-to-create-generative-art-in-less-than-100-lines-of-code-d37f379859f",
    "author" : "Eric Davidson"
}

class Sprites(EGWPluginGenerator):
    def __init__(self, **kwargs):
        super().__init__(**meta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_plugin_kwargs = { 'sprite_size' : random.randrange(3,99,2), # must be an odd integer
                              'invaders' : random.randint(1,60), # nr invaders per row
                              'file_out' : None,
                             }

        self._define_mandatory_kwargs(self, **add_plugin_kwargs)
        self.kwargs = kwargs

    def _generate_image(self):
        return _create_sprites(**self.kwargs)


generator = Sprites()
assert isinstance(generator,EGWPluginGenerator)

# --- .. here comes the plugin-specific part to get some work done...

from .sprites import main as _sprites_main

def _create_sprites(sprite_size = 13, invaders = 8, size = (600,600), file_out = None):
    """
    this is the wrapper around the functionality of the plugin.
    """
    if size[0] != size[1]:
        raise Exception("size must be a sqare")
    if sprite_size % 2 != 1:
        raise Exception("sprite_size must be an odd integer but is {}".format(sprite_size))
    return _sprites_main(size = sprite_size, invaders = invaders, img_size = size[0], file_out = file_out)
