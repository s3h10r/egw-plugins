#!/usr/bin/env python
#coding=utf-8
"""
usage example:

egw --generator psychedelic -o /tmp/2.png --filter puzzle -c ./einguteswerkzeug/einguteswerkzeug.conf --template ./einguteswerkzeug/templates/square/roland-deason-tPWHTBzQVIM-unsplash.jpg -s 200 --alpha-blend 0.8  --border-size 1 --nopolaroid --noframe --title="hallo" && feh /tmp/2.png
egw --generator psychedelic -o /tmp/2.png --filter puzzle -c ./einguteswerkzeug/einguteswerkzeug.conf --template ./einguteswerkzeug/templates/square/roland-deason-tPWHTBzQVIM-unsplash.jpg -s 200 --alpha-blend 0.8  --border-size 0.8 --nopolaroid --noframe --title="hallo" && feh /tmp/2.png
"""
import logging
import math
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
    "version" : "0.0.8",
    "description" : "",
    "author" : ""
}

class Puzzle(EGWPluginFilter):
    def __init__(self, **kwargs):
        super().__init__(**fmeta)
        # defining mandatory kwargs (addionals to the mandatory of the base-class)
        add_kwargs = { 'seed' : random.randrange(sys.maxsize), 'block_size' : 100}
        self._define_mandatory_kwargs(self, **add_kwargs)
        self.kwargs = kwargs


    def _generate_image(self):
        return _puzzle(**self.kwargs)


filter = Puzzle()
assert isinstance(filter,EGWPluginFilter)


def _puzzle(image = None, seed = None, block_size = 100):
    """
     10 <= block_size >= 2000
    """
    min_block_size = 10
    max_block_size = 2000
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    log.info("seed: {}".format(seed))

    im = image
    width, height = im.size
    if width != height:
        raise Exception("sorry, only square-sized image can be processed.")

    # --- adjusting block_size if necessary
    if width % block_size != 0:
        log.warning("{} % {} = {}. => adjusting blocksize.".format(width, block_size, width % block_size))
    block_size_orig = block_size
    while (width % block_size != 0) and block_size <= max_block_size:
        block_size += 1
    if (width % block_size != 0):
        block_size = block_size_orig
        while (width % block_size != 0) and (block_size >= min_block_size):
            block_size -= 1
    assert(width % block_size == 0)
    log.info("block_size adjusted to: {}".format(block_size))
    # ---

    im2 = Image.new("RGB", (width, height), "black")
    blocks = []
    for x in range(int(width / block_size)):
        for y in range(int(height / block_size)):
            blocks.append(im.crop((x * block_size, y * block_size, (x + 1) * block_size, (y + 1) * block_size)))
    random.shuffle(blocks)
    for x in range(int(width / block_size)):
        for y in range(int(height / block_size)):
            im2.paste(blocks.pop().rotate(90 * random.randint(0,3)), (x * block_size, y * block_size))
    return im2
