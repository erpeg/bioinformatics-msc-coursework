#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import utility as ut


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-s', '--show_save', type=str, help='presenting plot; mode: 0(showing plot), 1(saving plot to given path)')
    args = parser.parse_args()

    # assigning columns' to the proper axes
    x_axis = 'year'
    y_axis = 'AverageTemperatureCelsius'

    data = ut.data_for_scatter(args.input_file, xax=x_axis, yax=y_axis)

    fig, ax = plt.subplots(figsize=(7, 5))
    years = data[0]
    temps = data[1]

    for year, temp in zip(years, temps):
        ax.scatter([year] * len(temp), temp, color='black', s=20, alpha=0.05)

    ax.set_ylim(ut.max_min(temps)[2:4])

    # set title of axes
    ax.set_ylabel(y_axis, fontsize=15)
    ax.set_xlabel(x_axis, fontsize=15)

    # applying styles of plotting area
    ut.plot_gui_setup_scatter(ax, plt)

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        plt.savefig('plots/task2c.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()