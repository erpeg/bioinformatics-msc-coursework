#!/usr/bin/python3

import requests
import argparse
import sys
import csv
import pandas as pd
import numpy as np


def id_to_list(id, nodes):
    if nodes == None:
        nodes = 10
    elif int(nodes) < 1:
        print('Wrong nodes value.')
        sys.exit()
    else:
        pass

    url = 'https://string-db.org/api/tsv-no-header/network?identifiers='+str(id)+'&add_nodes='+str(nodes)

    response = requests.get(url)

    tsv = []

    for line in response.text.strip().split("\n"):
        tsv.append(line.strip().split("\t"))

    return tsv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--id_a', type=str, help='id of protein a')
    parser.add_argument('-b', '--id_b', type=str, help='id of protein b')
    parser.add_argument('-n', '--nodes', type=str, help='nodes; default 10')
    parser.add_argument('-o', '--output', type=str, help='name of output file')
    args = parser.parse_args()

    try:
        a_ids = []
        a_ids+=[line[3].upper() for line in id_to_list(args.id_a, args.nodes)]
        a_ids = list(set(a_ids))

        b_ids = []
        b_ids+=[line[3].upper() for line in id_to_list(args.id_b, args.nodes)]
        b_ids = list(set(b_ids))

        print('Comparing protein: ' + args.id_a + ' with ' + args.id_b)
        soon_csv = {}

        headers = ['common', 'new_in_a', 'lacks_in_a', 'new_in_b', 'lacks_in_b']

        for item_a in a_ids:
            # 1st loop checks if proteins of a are in b's proteins
            if item_a in b_ids:
                if headers[0] in soon_csv:
                    soon_csv[headers[0]].append(item_a)
                else:
                    soon_csv[headers[0]] = [item_a]
            if item_a not in b_ids:
                if headers[1] in soon_csv:
                    soon_csv[headers[1]].append(item_a)
                else:
                    soon_csv[headers[1]] = [item_a]

        for item_b in b_ids:
            if item_b not in a_ids:
                if headers[3] in soon_csv:
                    soon_csv[headers[3]].append(item_b)
                else:
                    soon_csv[headers[3]] = [item_b]

        soon_csv['lacks_in_a'] = soon_csv['new_in_b']
        soon_csv['lacks_in_b'] = soon_csv['new_in_a']

        df = pd.DataFrame.from_dict(soon_csv, orient='index').transpose()

        df.replace(np.nan, '', regex=True)
        df = df.reindex(columns=headers)
        df.to_csv(args.output, index=False)

        print('File was saved as '+str(args.output))
    except:
        print('Data were given unproperly.')


if __name__ == '__main__':
    main()