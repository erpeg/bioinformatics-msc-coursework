# Protein Network Neighbour Comparision
## Description
Softwer enables comparision of neighbours of selected proteins in two networks stored in string-db.org:
- common nodes
- nodes new in network a
- nodes lacking in network a
- nodes new in network b
- nodes lacking in network b

 App exports results in .csv format.

## Example usage
```{shell script}
./compare_proteins.py -a ENSP00000335153 -b FBpp0305095 -o homo_droso.csv -n 10
```

