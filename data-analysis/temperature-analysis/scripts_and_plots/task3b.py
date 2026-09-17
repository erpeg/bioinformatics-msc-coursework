#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import utility as ut
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-s', '--show_save', type=str, help='presenting plot; mode: 0(showing plot), 1(saving plot to given path)')
    args = parser.parse_args()

    # assigning columns' to the proper axes
    x_axis = 'country_id'
    y_axis = 'AverageTemperatureCelsius'

    data = ut.data_for_box(args.input_file, xax=x_axis, yax=y_axis)

    fig, ax = plt.subplots(figsize=(10, 7))
    country = data[0]
    temps = data[1]

    # plotting boxplot
    bp = plt.boxplot(temps, patch_artist=True, widths=0.5)
    ax.set_ylim(ut.max_min(temps)[2:4])

    # applying styles to boxes
    ut.boxes_style(bp)

    # add jitter
    for i in range(len(country)):
        y = temps[i]
        x = np.random.normal(1+i, 0.1, size=len(y))
        plt.plot(x, y, 'ro', alpha=0.2, color='orangered')

    # custom x-axis labels
    ax.set_xticklabels(country)

    # set title of axes
    ax.set_ylabel(y_axis, fontsize=15)
    ax.set_xlabel(x_axis, fontsize=15)

    # change fill color
    [box.set(facecolor='None') for box in bp['boxes']]

    # change whiskers level
    [whisker.set(zorder=3) for whisker in bp['whiskers']]

    # change fliers level
    [flier.set(zorder=3) for flier in bp['fliers']]

    # applying styles of plotting area
    ut.plot_gui_setup_box(ax, plt)

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        plt.savefig('plots/task3b.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()