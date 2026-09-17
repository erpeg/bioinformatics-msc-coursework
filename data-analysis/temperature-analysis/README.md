## Description
##### clean_temperatures.py is used to clean .csv file out of unnecessary data
## Functionality
* removing rows with 'NA' values
* converting Fahr to Celsius temperature
* removing unnecessary for visualization columns ('day')

#### Usage
Script takes 2 arguments:
* name of input file as -i
* name of output cleaned file as -o

#### Example usage
```
./clean_temperatures.py -i temperature.csv -o temperature_clean.csv
```