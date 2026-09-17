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
    x_axis = 'country_id'
    y_axis = 'AverageTemperatureCelsius'

    data = ut.data_for_box(args.input_file, xax=x_axis, yax=y_axis)

    fig, ax = plt.subplots(figsize=(10, 7))
    country = data[0]
    temps = data[1]

    # plotting boxplot
    bp = ax.violinplot(temps)
    ax.set_ylim(ut.max_min(temps)[2:4])

    country += 'A'
    country.sort()
    # custom x-axis labels
    ax.set_xticklabels(country)

    # set title of axes
    ax.set_ylabel(y_axis, fontsize=15)
    ax.set_xlabel(x_axis, fontsize=15)

    # applying styles of plotting area
    ut.plot_gui_setup_box(ax, plt)

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        plt.savefig('plots/task3c.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()