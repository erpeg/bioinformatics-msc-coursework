#!/usr/bin/env python3

import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='input .csv file')
    parser.add_argument('-o', '--output_file', type=str, help='output .csv file')
    parser.add_argument('-c', '--countries', nargs='+', help='countries to select')
    args = parser.parse_args()

    file = pd.read_csv(args.input_file)

    groups = [
        'East Asia & Pacific',
        'Europe & Central Asia',
        'Latin America & Caribbean',
        'Middle East & North Africa',
        'North America',
        'South Asia',
        'Sub-Saharan Africa',
        'Income levels',
        'High income',
        'Low & middle income',
        'Low income',
        'Lower middle income',
        'Middle income',
        'Upper middle income',
        'Lending Groups',
        'IBRD only',
        'IDA blend',
        'IDA only',
        'Demographic Dividend Groups',
        'Early-demographic dividend',
        'Late-demographic dividend',
        'Post-demographic dividend',
        'Pre-demographic dividend',
        'Small States',
        'Caribbean small states',
        'Other small states',
        'Pacific island small states',
        'Small states',
        'Other country groups',
        'Arab World',
        'Central Europe and the Baltics',
        'East Asia & Pacific (excluding high income)',
        'Euro area',
        'Europe & Central Asia (excluding high income)',
        'European Union',
        'Fragile and conflict affected situations',
        'Heavily indebted poor countries (HIPC)',
        'Latin America & Caribbean (excluding high income)',
        'Least developed countries: UN classification',
        'Middle East & North Africa (excluding high income)',
        'OECD members',
        'Sub-Saharan Africa (excluding high income)',
        'World',
        'IDA & IBRD total',
        'IDA total',
        'Not classified',
        'Macao SAR, China',
        'East Asia & Pacific (IDA & IBRD countries)',
        'Europe & Central Asia (IDA & IBRD countries)',
        'Latin America & the Caribbean (IDA & IBRD countries)',
        'Middle East & North Africa (IDA & IBRD countries)',
        'South Asia (IDA & IBRD)',
        'Sub-Saharan Africa (IDA & IBRD countries)'
    ]

    for group in groups:
        file = file[file['Country Name'] != group]

    del file['Indicator Name']
    del file['Indicator Code']
    del file['2019']
    del file['Unnamed: 64']

    selected_countries = file[file['Country Name'].isin(args.countries)]

    selected_countries.to_csv(args.output_file, index=False)


if __name__ == '__main__':
    main()