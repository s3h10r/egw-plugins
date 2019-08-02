#!/bin/bash -vx
FOUT=$(realpath "./egw_plugin_nlines.selftest.png")
CMD=$(realpath "./egw_plugin_nlines.py")
SEED1="8266149732682978900"
FOUT1=$(realpath "./egw_plugin_nlines.selftest.seed_${SEED1}.png")

$CMD $FOUT || exit 1
feh $FOUT

$CMD $FOUT1 $SEED1 || exit 1
feh $FOUT1
