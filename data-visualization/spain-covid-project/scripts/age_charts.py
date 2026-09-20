#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import matplotlib.ticker as plticker

df = pd.read_csv('data/datasets/COVID_19/nacional_covid19_rango_edad.csv')
df = df[df.rango_edad != 'Total']
df = df[df.rango_edad != '90 y +']
df = df[df.fecha != '2020-03-23']
df = df[df.fecha != '2020-03-24']
df = df[df.fecha != '2020-03-25']

df = df.drop(['hospitalizados', 'ingresos_uci'], axis=1)
df = df.reset_index().drop('index', axis=1)
df.columns = ['Time', 'Age range', 'Sex', 'Cases confirmed', 'Deceased']

df_both = df[df.Sex == 'ambos']
df_female = df[df.Sex == 'mujeres']
df_male = df[df.Sex == 'hombres']

all_dfs = [df_both, df_female, df_male]

dict_both_cases = df_both.groupby('Time')['Cases confirmed'].apply(list).to_dict()
dict_both_deaths = df_both.groupby('Time')['Deceased'].apply(list).to_dict()

dict_female_cases = df_female.groupby('Time')['Cases confirmed'].apply(list).to_dict()
dict_female_deaths = df_female.groupby('Time')['Deceased'].apply(list).to_dict()

dict_male_cases = df_male.groupby('Time')['Cases confirmed'].apply(list).to_dict()
dict_male_deaths = df_male.groupby('Time')['Deceased'].apply(list).to_dict()

fig, ax = plt.subplots()

day01_bar = dict_both_cases['2020-03-27']
day01_line = dict_both_deaths['2020-03-27']

age_ranges = list(range(0, len(day01_bar)))

age_ticks = [df_female['Age range'].values[0]] + list(df_female['Age range'].values[0:9])

days = list(dict_both_cases.keys())

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 8))

gif_name = 'age_charts.gif'

lol = list(dict_both_cases.values())
both_cases = list(dict_both_cases.values())


def animate(i):
    for ax in [ax1, ax2, ax3]:
        ax.clear()
        ax.set_ylim(top=45000)
        ax.set_xticklabels(age_ticks, rotation=45)
        loc = plticker.MultipleLocator(base=1.0)  # this locator puts ticks at regular intervals
        ax.xaxis.set_major_locator(loc)
    ax1.set_title('Total')
    ax2.set_title('Male')
    ax3.set_title('Female')
    ax1.bar(age_ranges, height=both_cases[i], color='grey')
    ax2.bar(age_ranges, height=list(dict_female_cases.values())[i], color='dodgerblue')
    ax3.bar(age_ranges, height=list(dict_male_cases.values())[i], color='indianred')
    ax1.bar(age_ranges, height=list(dict_both_deaths.values())[i], color='black')
    ax2.bar(age_ranges, height=list(dict_female_deaths.values())[i], color='black')
    ax3.bar(age_ranges, height=list(dict_male_deaths.values())[i], color='black')

    fig.suptitle(f'Confirmed cases and mortality of COVID-19 on {days[i]}')

    return ax1, ax2, ax3


anim = FuncAnimation(fig, animate, frames=52, interval=115, blit=False)

anim.save(gif_name, writer='imagemagick')

