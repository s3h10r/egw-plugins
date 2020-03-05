#!/bin/bash -vx
rm -i ./*png

FOUT=$(realpath "./egw_plugin_rothko.selftest.png")
CMD=$(realpath "./egw_plugin_rothko.py")
$CMD $FOUT || exit 1
feh $FOUT

# No. 1372403442 (Free Orange, Hazel, and Deep Sea Blue on Dark Blue Grey)
# No. 988209721 (Light Blue Grey, Dark Grey Blue, and Blush Pink on Green Blue)
# ... etc.pp.
SEEDS=('1372403442' '988209721' '1703988514' '1703988515' '1452541309')
for seed in "${SEEDS[@]}"
do
  FOUT=$(realpath "./egw_plugin_rothko.selftest.seed_${seed}.png")
  echo "...creating ${FOUT}"
  $CMD $FOUT $seed || exit 1
done
feh ./*png
