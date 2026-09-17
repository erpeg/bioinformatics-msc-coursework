#!/usr/bin/python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import utility as ut
import matplotlib.cm as cm
import numpy as np
import matplotlib.patches as mpatches

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-s', '--show_save', type=str, help='presenting plot; mode: 0(showing plot), 1(saving plot to given path)')
    args = parser.parse_args()

    df = pd.read_csv(filepath_or_buffer=args.input_file)

    trans_dict = ut.trans_of_shorts(args.input_file)

    values = df.groupby(['country_id', 'year', 'City'])['AverageTemperatureCelsius'].mean()
    grouped_data = df.groupby(['country_id']).apply(lambda grp: grp.groupby('year')['AverageTemperatureCelsius'].mean().to_dict()).to_dict()

    # assigning columns' to the proper axes
    x_axis = 'year'
    y_axis = 'CountryAverage'

    fig, ax = plt.subplots(figsize=(10, 7))

    # crea
    countries_to_legend = list(grouped_data.keys())
    countries_to_legend.sort()
    colors = cm.gist_rainbow(np.linspace(0, 1, len(countries_to_legend)))   # create array of colors
    colors = np.delete(colors, -1, axis=1)  # remove alpha column
    colors[:, 0:3] *= 0.8    # darken colors

    # country_id:color
    dict_of_colors = {}
    for country, color in zip(countries_to_legend, colors):
        dict_of_colors[country] = color

    dict_for_legend = {}

    # plotting and translating country_ids to countries to ax.legend()
    for country, temps_per_year in grouped_data.items():
        dict_for_legend[trans_dict[country]] = dict_of_colors[country]  # translate country_ids to full countries in new dict
        ax.plot(list(temps_per_year.keys()), list(temps_per_year.values()), color=dict_of_colors[country], alpha=0.8, linewidth=2, label=trans_dict[country])

    # add and customize legend
    plt.legend(dict_for_legend)
    handles, labels = ax.get_legend_handles_labels()
    black_patch = mpatches.Patch(color='gainsboro', alpha=0.5)
    handles = [(black_patch, handle) for handle in handles]
    plt.legend(handles, labels, title='$\\bf{Country}$', title_fontsize=19, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, fontsize=16, handlelength=2, handleheight=1.5)._legend_box.align = "left"

    # set title of axes
    ax.set_ylabel(y_axis, fontsize=18)
    ax.set_xlabel(x_axis, fontsize=18)

    # applying styles of plotting area
    ut.plot_gui_setup_time(ax, plt)

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        plt.savefig('plots/task4c.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()