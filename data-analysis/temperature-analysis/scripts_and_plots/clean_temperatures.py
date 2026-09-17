#!/usr/bin/python

import argparse
import csv

def file_to_nested_list(file_name):
    with open(file_name) as file:
        file = file.read().split('\n')
        file = [line.replace('\"', '').split(',') for line in file]
    return file

# checking if any value of list is equal to 'NA'
def if_na(list):
    for element in list:
        if element == 'NA':
            return False
    return True

# fahr to celsius converter
def fahr_to_cel(fahr):
    try:
        if fahr == 'AverageTemperatureFahr':
            fahr = 'AverageTemperatureCelsius'
            return fahr
        elif fahr == 'AverageTemperatureUncertaintyFahr':
            fahr = 'AverageTemperatureUncertaintyCelsius'
            return fahr
        else:
            celsius = round((float(fahr) - 32) * 5/9, 4)
            return celsius
    except:
        print('Improper data given')

def main():
    # creating a parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_name', type=str, help='path to input .csv file')
    parser.add_argument('-o', '--out_name', type=str, help='name of output file')
    args = parser.parse_args()

    list_of_temps = file_to_nested_list(args.input_name)
    nr_categories = len(list_of_temps[0])

    # removing incomplete lines
    list_of_temps = [line for line in list_of_temps if len(line) == nr_categories]

    # removing lines with 'NA' values
    new_list = [line for line in list_of_temps if if_na(line)]

    col_names = new_list[0]

    for line in new_list:
        # removing day column
        line.pop(2)
        # converting fahrenheit to celsius
        line[3] = fahr_to_cel(line[3])
        line[4] = fahr_to_cel(line[4])
        for i in range(0, 3):    # converting first 3 cols to int
            if line[i] in col_names:
                break
            else:
                line[i] = int(line[i])

    # saving to file
    if args.out_name:
        with open(args.out_name, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_list)
        print('File saved as: ' + str(args.out_name))
    # showing first 10 rows
    else:
        for line in new_list[0:10]:
            print(line)

if __name__ == '__main__':
    main()
