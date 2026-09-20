#!/usr/bin/python3

import csv
import collections
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import colorsys
from matplotlib.colors import LinearSegmentedColormap as lsc

# possible key_value: year, country_id, Country
def dict_to_plot(list, x_axis, y_axis):
    # creating dictionary of column indexes
    col_dict = {}
    col_names = list[0]
    for value, key in enumerate(list[0]):
        col_dict[key] = value
    # using col_dict to index by passed in the function name of column
    temps_dict = collections.OrderedDict()
    try:
        for line in list[1:]:
            if line[col_dict[x_axis]] in temps_dict:
                temps_dict[line[col_dict[x_axis]]].append(line[col_names.index(y_axis)])
            else:
                temps_dict[line[col_dict[x_axis]]] = [line[col_names.index(y_axis)]]
    except:
        print('Improper names of axises')
    return temps_dict

def max_min(values_list):
    try:
        max_temp = round(max([max(temp) for temp in values_list]), 0)
        min_temp = round(min([min(temp) for temp in values_list]), 0)
        max_temp_mod = max_temp + 2
        min_temp_mod = min_temp - 2
    except:
        max_temp = round(max(values_list), 0)
        min_temp = round(min(values_list), 0)
        max_temp_mod = max_temp + 10
        min_temp_mod = min_temp - 10
    return min_temp, max_temp, min_temp_mod, max_temp_mod

def open_file(file):
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        file = [row for row in reader]
    return file

def data_for_scatter(file_path, xax, yax):
    file_list = open_file(file_path)
    col_names = file_list[0]
    data = dict_to_plot(file_list, x_axis=xax, y_axis=yax)

    # create ordered dict
    ordered_data = collections.OrderedDict()

    # sorting loaded dict
    for key in sorted(data):
        ordered_data[key] = [float(element) for element in data[key]]

    years = [int(year) for year in ordered_data.keys()][::-1]
    temps = [temps for temps in ordered_data.values()][::-1]

    return years, temps, col_names

def data_for_box(file_path, xax, yax):
    file_list = open_file(file_path)
    col_names = file_list[0]
    data = dict_to_plot(file_list, x_axis=xax, y_axis=yax)

    # create ordered dict
    ordered_data = collections.OrderedDict()

    # sorting loaded dict
    for key in sorted(data):
        ordered_data[key] = [float(element) for element in data[key]]

    country = [country for country in ordered_data.keys()]
    temps = [temps for temps in ordered_data.values()]

    return country, temps, col_names

# main styles of plot and labels
def main_style(ax, plt):
    # background and grid
    ax.set_axisbelow(True)  # grid behind scatter
    ax.set_facecolor('0.85') # background colour
    ax.grid(which='major', b=True, linestyle='-', linewidth=1.5, color='0.95')
    ax.grid(which='minor', b=True, linestyle='-', linewidth=.5, color='0.95')


    # set properties of ticks
    plt.xticks(color='gray', alpha=0.7)
    plt.yticks(color='gray', alpha=0.7)
    ax.tick_params(which='major', labelsize=15, length=5, width=1, color='0.7') # showing major spines
    ax.tick_params(which='minor', color='1') # hiding minor spines

    # hiding frames
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return ax, plt

def plot_gui_setup_scatter(ax, plt):
    # setting values of ticks for future grid
    major_xticks = np.arange(1800, 2100, 100)
    major_yticks = np.arange(-10, 40, 10)
    minor_xticks = np.arange(1750, 2000, 50)
    minor_yticks = np.arange(-15, 30, 5)

    ax.set_xticks(major_xticks)
    ax.set_yticks(major_yticks)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)

    main_style(ax, plt)
    return ax, plt

def plot_gui_setup_box(ax, plt):
    # setting values of ticks for future grid
    major_yticks = np.arange(-10, 40, 10)
    minor_yticks = np.arange(-15, 30, 5)
    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor=True)

    main_style(ax, plt)
    return ax, plt

def plot_gui_setup_time(ax, plt):
    # setting values of ticks for future grid
    major_xticks = np.arange(1800, 2100, 100)
    major_yticks = np.arange(0, 25, 5)
    minor_xticks = np.arange(1750, 2000, 50)
    minor_yticks = np.arange(-5, 20, 2.5)

    ax.set_xticks(major_xticks)
    ax.set_yticks(major_yticks)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)

    main_style(ax, plt)
    return ax, plt

def plot_gui_setup_time_many(ax, plt):
    # setting values of ticks for future grid
    major_xticks = np.arange(1800, 2100, 100)
    major_yticks = np.arange(0, 25, 5)
    minor_xticks = np.arange(1750, 2000, 50)
    minor_yticks = np.arange(-5, 25, 2.5)

    ax.set_xticks(major_xticks)
    ax.set_yticks(major_yticks)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)

    main_style(ax, plt)
    return ax, plt

def boxes_style(bp):
    # change color and linewidth of the medians
    [median.set(color='black', linewidth=2) for median in bp['medians']]

    # change color and linewidth of the caps
    [cap.set(linewidth=0) for cap in bp['caps']]

    return bp

def trans_of_shorts(file):
    data = open_file(file)
    dict_of_shorts = {}

    for row in data:
        if row[6] not in dict_of_shorts.keys():
            dict_of_shorts[row[6]] = row[7]
    return dict_of_shorts

# main styles of plot and labels
def main_style_white(ax, plt):
    # background and grid
    ax.set_axisbelow(True)  # grid behind scatter
    ax.set_facecolor('1') # background colour
    ax.grid(which='major', b=True, linestyle='-', linewidth=1.5, color='0.8')
    ax.grid(which='minor', b=True, linestyle='-', linewidth=.5, color='0.85')


    # set properties of ticks
    plt.xticks(color='gray', alpha=0.7)
    plt.yticks(color='gray', alpha=0.7)
    ax.tick_params(which='major', labelsize=15, length=5, width=1, color='0.7') # showing major spines
    ax.tick_params(which='minor', color='1') # hiding minor spines

    # hiding frames
    return ax, plt

def plot_gui_setup_time_many_white(ax, plt):
    # setting values of ticks for future grid
    major_xticks = np.arange(1800, 2100, 100)
    major_yticks = np.arange(0, 25, 5)
    minor_xticks = np.arange(1750, 2000, 50)
    minor_yticks = np.arange(-5, 25, 2.5)

    ax.set_xticks(major_xticks)
    ax.set_yticks(major_yticks)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(minor_yticks, minor=True)

    main_style_white(ax, plt)
    return ax, plt



