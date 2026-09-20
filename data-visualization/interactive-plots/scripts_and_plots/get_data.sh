#!/usr/bin/env bash

mkdir -p ../data
echo "If data dir didn't exist, it has been created. All files will be saved there."

python3 ./prepare_data.py -i ../data/full_database.csv -o ../data/data1.csv -c Poland Germany "Czech Republic" Slovenia Ukraine
echo "data1.csv saved."
python3 ./prepare_data.py -i ../data/full_database.csv -o ../data/data2.csv -c "Saudi Arabia" Oman Jordan Iraq "Yemen, Rep."
echo "data2.csv saved."
python3 ./prepare_data.py -i ../data/full_database.csv -o ../data/data3.csv -c Japan China Mongolia Philippines Vietnam
echo "data3.csv saved."
python3 ./prepare_data.py -i ../data/full_database.csv -o ../data/data4.csv -c India "Sri Lanka" Bangladesh Pakistan Nepal
echo "data4.csv saved."
python3 ./prepare_data.py -i ../data/full_database.csv -o ../data/data5.csv -c Romania Moldova Bulgaria Hungary Ukraine
echo "data5.csv saved."
python3 ./prepare_data.py -i ../data/full_database.csv -o ../data/data6.csv -c Spain Italy Portugal France Hungary
echo "data6.csv saved."