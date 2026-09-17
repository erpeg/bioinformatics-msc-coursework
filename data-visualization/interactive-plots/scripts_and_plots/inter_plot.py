#!/usr/bin/env python3

import pandas as pd
import argparse
import altair as alt
import plotly.express as px
from bokeh.io import show, output_file, save
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-o', '--output_file', type=str, help='output file name')
    parser.add_argument('-t', '--type', type=str, choices=['alt_line', 'alt_highlight', 'bokeh', 'plotly_exp'], help='library')
    args = parser.parse_args()

    file = pd.read_csv(args.input_file)

    acro_to_country = {}

    for i in range(len(file['Country Code'])):
        acro_to_country[file['Country Code'][i]] = file['Country Name'][i]

    # preparing dataframe for altair plots
    file_for_altair = file.T
    file_for_altair = file_for_altair.drop('Country Code')
    file_for_altair.columns = file_for_altair.iloc[0]
    file_for_altair = file_for_altair.drop('Country Name')
    file_for_altair = file_for_altair.reset_index()

    # metling dataframe for altair
    source = file_for_altair.melt('index', var_name='category', value_name='y')

    # renaming columns
    source.columns = ['Years', 'Country', 'Population']

    if args.type == 'alt_line':

        # choosing closes point
        nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['Years'], empty='none')

        # drawing all lines
        line = alt.Chart(source).mark_line(interpolate='basis').encode(x='Years:Q', y='Population:Q', color='Country:N')

        # creating selector of points
        selectors = alt.Chart(source).mark_point().encode(x='Years:Q', opacity=alt.value(0),).add_selection(nearest)

        # preparing marker points
        points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

        # preparing labels next to marker points
        text = line.mark_text(align='left', dx=5, dy=-15).encode(text=alt.condition(nearest, 'Population:Q', alt.value(' ')))

        # adjusting location of sleection
        rules = alt.Chart(source).mark_rule(color='gray').encode(x='Years:Q',).transform_filter(nearest)

        # combining all layers
        final = alt.layer(line, selectors, points, rules, text).properties(width=700, height=400)

        if args.output_file:
            alt.Chart.save(final, args.output_file)
            print('Plot ' + args.output_file + ' saved.')
        else:
            alt.Chart.show(final)

    if args.type == 'alt_highlight':
        highlight = alt.selection(type='single', on='mouseover', fields=['Country'], nearest=True)

        base = alt.Chart(source).encode(x='Years:T', y='Population:Q', color='Country:N')

        points = base.mark_circle().encode(opacity=alt.value(0)).add_selection(highlight).properties(width=600)

        lines = base.mark_line().encode(size=alt.condition(~highlight, alt.value(1), alt.value(3)))

        final = points + lines

        if args.output_file:
            alt.Chart.save(final, args.output_file)
            print('Plot ' + args.output_file + ' saved.')
        else:
            alt.Chart.show(final)

    if args.type == 'plotly_exp':

        fig = px.line(source, x='Years', y='Population', color='Country')

        if args.output_file:
            fig.write_html(args.output_file)
            print('Plot ' + args.output_file + ' saved.')
        else:
            fig.show()


    if args.type == 'bokeh':
        df_bokeh = file.T
        df_bokeh.reset_index()
        df_bokeh.columns = df_bokeh.iloc[0]
        countries = [country for country in df_bokeh.iloc[0]]
        colors_for_countries = ['red', 'blue', 'orange', 'magenta', 'green']

        df_bokeh = df_bokeh.drop('Country Name')
        df_bokeh = df_bokeh.drop('Country Code')
        df_bokeh = df_bokeh.reset_index()
        df_bokeh = df_bokeh.rename(columns={'index': 'Years'})

        years = df_bokeh['Years'].tolist()

        p = figure(title='Population of countries throught the years')

        for nr, country in enumerate(countries):
            country_list = []
            color = []
            for year in years:
                country_list.append(country)
                color.append(colors_for_countries[nr])

            source = ColumnDataSource(data=dict(
                Year=years,
                Population=df_bokeh[country].tolist(),
                Country=country_list
            ))
            p.line('Year', 'Population', source=source, color=colors_for_countries[nr])
        show(p)

        if args.output_file:
            output_file(args.output_file, title='Population of selected countries throughout the years')
            save(p)
        else:
            show(p)

if __name__ == '__main__':
    main()