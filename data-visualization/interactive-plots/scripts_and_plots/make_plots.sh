#!/usr/bin/env bash

cd ..
mkdir -p plots
for file in data/data* ; do
  filename=$(basename $file)
  filename_wo_ext=${filename:0:-4}
  python3 ./scripts_and_plots/inter_plot.py -i $file -t alt_line -o plots/${filename_wo_ext}_alt_line.html
  python3 ./scripts_and_plots/inter_plot.py -i $file -t alt_highlight -o plots/${filename_wo_ext}_alt_highlight.html
  python3 ./scripts_and_plots/inter_plot.py -i $file -t plotly_exp -o plots/${filename_wo_ext}_plotly_exp.html
  python3 ./scripts_and_plots/inter_plot.py -i $file -t bokeh -o plots/${filename_wo_ext}_bokeh.html
done
