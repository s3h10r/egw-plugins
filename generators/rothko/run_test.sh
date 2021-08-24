#!/bin/bash -vx
rm -i ./*png

FOUT=$(realpath "./egw_plugin_rothko.selftest.png")
CMD=$(realpath "./egw_plugin_rothko.py")
$CMD $FOUT || exit 1
feh -Z -F $FOUT

# No. 1372403442 (Free Orange, Hazel, and Deep Sea Blue on Dark Blue Grey)
# No. 1551414546 (Pinky Pink, Orange Pink, and Taupe on Pebble Gray)
# No. 988209721 (Light Blue Grey, Dark Grey Blue, and Blush Pink on Green Blue)
# ... etc.pp.
SEEDS=('495039745' '839605687' '1372403442' '1551414546' '988209721' '1703988514' '1703988515' '1452541309')
for seed in "${SEEDS[@]}"
do
  FOUT=$(realpath "./egw_plugin_rothko.selftest.seed_${seed}.png")
  echo "...creating ${FOUT}"
  $CMD $FOUT $seed || exit 1
done
feh -Z -F ./*png
