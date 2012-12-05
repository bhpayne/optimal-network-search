#!/bin/bash

picsDir=picture_frames
numberOfFrames=5

rm -rf $picsDir
mkdir $picsDir

python generate_graph.py
python generate_graphViz_plot.py
mv network_circo.png network_circo_0.png 
mv network_circo_0.png $picsDir

for (( indx=1; indx<=$numberOfFrames; indx++ ))
do
  python make_alterations_to_graph.py
  python generate_graphViz_plot.py
  mv network_circo.png network_circo_${indx}.png 
  mv network_circo_${indx}.png $picsDir
done

