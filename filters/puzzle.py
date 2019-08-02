#!/usr/bin/env python
#coding=utf-8
import logging
import random
import string
import sys
from PIL import Image, ImageDraw
from PIL import Image
from einguteswerkzeug.plugins import EGWPluginFilter

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

fmeta = {
    "name" : "puzzle",
    "version" : "0.0.3",
    "description" : "",
    "author" : "codegolf"
}

class Puzzle(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'seed' : random.randrange(sys.maxsize) }
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def _generate_image(self):
        return _puzzle(**self.kwargs)


filter = Puzzle()
assert isinstance(filter,EGWPluginFilter)


def _puzzle(image = None, seed = None):
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    log.info("seed: {}".format(seed))

    im = image
    width, height = im.size
    width = int( ((width + 99) / 100) * 100 )
    height = int( ((int(height + 99) / 100)) * 100 )
    im = im.crop((0, 0, width, height))
    im2 = Image.new("RGB", (width, height), "black")
    blocks = []
    for x in range(int(width / 100)):
        for y in range(int(height / 100)):
            blocks.append(im.crop((x * 100, y * 100, (x + 1) * 100, (y + 1) * 100)))
    random.shuffle(blocks)
    for x in range(int(width / 100)):
        for y in range(int(height / 100)):
            im2.paste(blocks.pop().rotate(90 * random.randint(0,3)), (x * 100, y * 100))
    return im2
