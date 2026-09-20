#!/usr/bin/python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import utility as ut
import matplotlib.cm as cm
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnchoredText

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-s', '--show_save', type=str, help='presenting plot; mode: 0(showing plot), 1(saving plot to given path)')
    args = parser.parse_args()

    df = pd.read_csv(filepath_or_buffer=args.input_file)

    trans_dict = ut.trans_of_shorts(args.input_file)

    values = df.groupby(['country_id', 'year', 'City'])['AverageTemperatureCelsius'].mean()
    grouped_data = df.groupby(['country_id']).apply(lambda grp : grp.groupby(['City']).apply(lambda grp: grp.groupby('year')['AverageTemperatureCelsius'].mean().to_dict()).to_dict()).to_dict()

    # assigning columns' to the proper axes
    x_axis = 'year'
    y_axis = 'CityAverage'

    placing_plots = {
        'BRA':[0, 0],
        'FRA':[0, 1],
        'JAP':[0, 2],
        'NEW':[1, 0],
        'POL':[1, 1],
        'SOU':[1, 2],
        'SWE':[2, 0],
        'UKR':[2, 1]
    }

    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(10, 7), sharex=True, sharey=True)

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
    axes = []
    list_for_legend = []

    # plotting and translating country_ids to countries to ax.legend()
    for country, city_data in grouped_data.items():
        for city, temps_per_year in city_data.items():

            dict_for_legend[trans_dict[country]] = dict_of_colors[country]  # translate country_ids to full countries in new dict
            l, = axs[placing_plots[country][0], placing_plots[country][1]].plot(list(temps_per_year.keys()), list(temps_per_year.values()), color=dict_of_colors[country], alpha=0.8, linewidth=2, label=city)
            title = axs[placing_plots[country][0], placing_plots[country][1]].set_title(trans_dict[country], backgroundcolor='silver')
            title._bbox_patch._mutation_aspect = 0.03

            # applying styles of plotting area
            ut.plot_gui_setup_time_many_white(axs[placing_plots[country][0], placing_plots[country][1]], plt)

            if placing_plots[country][1] in [1, 2]:
                if placing_plots[country][0] != 2:
                    axs[placing_plots[country][0], placing_plots[country][1]].tick_params(which='major', color='1')

            # setting titlebox background
            if placing_plots[country][0] == 0:
                if country == 'FRA':
                    title.get_bbox_patch().set_boxstyle("square", pad=7.02)
                elif country == 'JAP':
                    title.get_bbox_patch().set_boxstyle("square", pad=7.35)
                else:
                    plt.xticks(color='white')
                    title.get_bbox_patch().set_boxstyle("square", pad=7.3)
            elif placing_plots[country][0] == 1:
                if country == 'NEW':
                    plt.xticks(color='white')
                    title.get_bbox_patch().set_boxstyle("square", pad=5.4)
                elif country == 'POL':
                    title.get_bbox_patch().set_boxstyle("square", pad=7.)
                else:
                    title.get_bbox_patch().set_boxstyle("square", pad=5.7)
            else:
                if country == 'UKR':
                    plt.xticks(color='gray', alpha=0.7)
                    title.get_bbox_patch().set_boxstyle("square", pad=6.73)
                else:
                    title.get_bbox_patch().set_boxstyle("square", pad=6.7)
            axes.append(l)
        list_for_legend.append(trans_dict[country])


    # set title of axes
    axs[placing_plots['NEW'][0], placing_plots['NEW'][1]].set_ylabel(y_axis, fontsize=18)
    axs[placing_plots['NEW'][0], placing_plots['NEW'][1]].set_xlabel(x_axis, fontsize=18)
    axs[2, 1].set_xlabel('year', fontsize=18)

    fig.legend(axes, list_for_legend, title='$\\bf{Country}$', title_fontsize=19, borderaxespad=0, loc='center right', frameon=False, fontsize=16, handlelength=2, handleheight=1.5)._legend_box.align = "left"

    plt.subplots_adjust(right=2)

    for ax in axs.flat:
        ax.label_outer()

    # removing one of plots
    axs[2, 2].remove()


    # # add and customize legend
    # plt.legend(dict_for_legend)
    # handles, labels = axs.get_legend_handles_labels()
    # black_patch = mpatches.Patch(color='gainsboro', alpha=0.5)
    # handles = [(black_patch, handle) for handle in handles]
    # plt.legend(handles, labels, title='$\\bf{Country}$', title_fontsize=19, loc='center left', bbox_to_anchor=(1, 0.5),
    #            frameon=False, fontsize=16, handlelength=2, handleheight=1.5)._legend_box.align = "left"

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        fig.set_size_inches(5.28, 8, forward=True)
        plt.savefig('plots/task5c.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()