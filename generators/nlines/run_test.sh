#!/bin/bash -vx
FOUT=$(realpath "./egw_plugin_nlines.selftest.png")
CMD=$(realpath "./egw_plugin_nlines.py")

$CMD $FOUT || exit 1

feh $FOUT
