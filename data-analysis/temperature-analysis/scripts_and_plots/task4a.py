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

    # sorting dataframe
    df.sort_values(by=['year', 'country_id'])

    # grouping by countries and getting dataframe of countries:years
    years = df.groupby(['country_id'])['year'].apply(list)

    # getting each year to one list and sorting it
    proper_years = []
    for series in years[::1]:
        proper_years += list(set(series))
    proper_years.sort()

    # calculating mean per year, per country and saving it to one list
    temps = df.groupby(['year', 'country_id'])['AverageTemperatureCelsius'].mean()
    temperatures = [temp for temp in temps]

    # assigning columns' to the proper axes
    x_axis = 'year'
    y_axis = 'CountryAverage'

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(proper_years, temperatures, color='black')

    # set title of axes
    ax.set_ylabel(y_axis, fontsize=15)
    ax.set_xlabel(x_axis, fontsize=15)

    # applying styles of plotting area
    ut.plot_gui_setup_time(ax, plt)

    print('Plotting fig')
    if args.show_save == '0':
        plt.show()
    else:
        plt.savefig('plots/task4a.png', bbox_inches='tight')
        print('Saving plot in plots dir.')
    print('Done')

if __name__ == '__main__':
    main()