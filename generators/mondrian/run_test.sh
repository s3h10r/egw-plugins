#!/bin/bash -vx
FOUT=$(realpath "./egw_plugin_mondrian.selftest.png")
CMD=$(realpath "./egw_plugin_mondrian.py")
SEED1="8266149732682978900"
FOUT1=$(realpath "./egw_plugin_mondrian.selftest.seed_${SEED1}.png")

$CMD 

$CMD $FOUT || exit 1
feh $FOUT

$CMD $FOUT1 $SEED1 || exit 1
feh $FOUT1
