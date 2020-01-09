#!/usr/bin/env python3

from projects import projects

def read_data(filename="data.txt"):
    file = open(filename, "r")
    lines = file.readlines()

    extracted_data = dict()

    for line in lines:
        (name, permutation) = line.split('|')
        extracted_data[name] = list()   

        for number in permutation.split(','):
            extracted_data[name].append(int(number))

    file.close()

    return extracted_data

project_permutation = read_data()

print(project_permutation)