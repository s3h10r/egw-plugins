#!/bin/bash -vx
FOUT=$(realpath "./egw_plugin_mondrian.selftest.png")
CMD=$(realpath "./egw_plugin_mondrian.py")

$CMD $FOUT || exit 1

feh $FOUT
