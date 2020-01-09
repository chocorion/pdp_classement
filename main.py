#!/usr/bin/env python3

from projects import projects

NUMBER_PROJECTS = 25

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


def make_project_popularity(student_permutation, display=False):
    result = dict()
    number_project_list = range(1, NUMBER_PROJECTS + 1)

    for i in number_project_list:
        result[i] = [0 for i in number_project_list]

    #print(result)

    for student in student_permutation.keys():
        for permutation_index in range(len(number_project_list)):
            #print(student_permutation[student], permutation_index, student_permutation[student][permutation_index])
            result[student_permutation[student][permutation_index]][permutation_index] += 1


    if (display):
        for project_num in number_project_list:
            print("{}.{:65s}\t{}".format(project_num, projects[project_num], result[project_num]))

    return result

project_permutation = read_data()

popularity = make_project_popularity(project_permutation, display=True)