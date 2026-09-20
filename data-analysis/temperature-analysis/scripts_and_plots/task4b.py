#!/usr/bin/python3
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import utility as ut


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-s', '--show_save', type=str, help='presenting plot; mode: 0(showing plot), 1(saving plot to given path)')
    args = parser.parse_args()

    df = pd.read_csv(filepath_or_buffer=args.input_file)
    values = df.groupby(['country_id', 'year', 'City'])['AverageTemperatureCelsius'].mean()
    grouped_data = df.groupby(['country_id']).apply(lambda grp: grp.groupby('year')['AverageTemperatureCelsius'].mean().to_dict()).to_dict()

    # assigning columns' to the proper axes
    x_axis = 'year'
    y_axis = 'CountryAverage'

    fig, ax = plt.subplots(figsize=(10, 7))

    countries_to_legend = list(grouped_data.keys())
    for country, temps_per_year in grouped_data.items():
        ax.plot(list(temps_per_year.keys()), list(temps_per_year.values()), color='black')

    # set title of axes
    ax.set_ylabel(y_axis, fontsize=15)
    ax.set_xlabel(x_axis, fontsize=15)

    # applying styles of plotting area
    ut.plot_gui_setup_time(ax, plt)

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        plt.savefig('plots/task4b.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()