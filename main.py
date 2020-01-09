#!/usr/bin/env python3

import sys
from random import shuffle
from projects import projects


NUMBER_PROJECTS = 25
GROUP_SIZE      = 5


def read_student_permutation_data(filename="data.txt"):
    ''' Read the permutation for each student, and return the dict '''
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
    ''' For each project, compute how many student want it on which position '''
    result = dict()
    number_project_list = range(1, NUMBER_PROJECTS + 1)

    for i in number_project_list:
        result[i] = [0 for i in number_project_list]


    for student in student_permutation.keys():
        for permutation_index in range(len(number_project_list)):
            result[student_permutation[student][permutation_index]][permutation_index] += 1


    if (display):
        print("\tProject popularity :\n\n")
        for project_num in number_project_list:
            print("{}.{:65s}\t{}".format(project_num, projects[project_num], result[project_num]))
        print('\n\n')

    return result



def generate_random_distribution(student_list, student_project_permutation, display=False):
    ''' Generate one distribution, based on a random permutation of students '''
    random_permutation = [i for i in range(len(student_list))]
    shuffle(random_permutation)

    student_per_project = dict()
    student_assigned_project = dict()

    for project_num in projects.keys():
        student_per_project[project_num] = 0

    for student_index in random_permutation:
        for choice in student_project_permutation[student_list[student_index]]:

            if student_per_project[choice] < GROUP_SIZE:
                student_per_project[choice] += 1
                student_assigned_project[student_list[student_index]] = choice
                break
        else: # Oui j'ai le droit de faire ça :)
            print("Error -> student without project !")
            sys.exit(0)

    if (display):
        print('\tOne distribution :\n\n')
        for project_num in projects.keys():
            project_student_list = list()

            for student in student_list:
                if student_assigned_project[student] == project_num:
                    project_student_list.append(student)

            print("{}.{:65s}\t -> {}".format(project_num, projects[project_num], project_student_list))
        print('\n')

    return student_assigned_project

    

def distribution_loss(student_assigned_project, student_project_permutation):
    loss = 0

    for student in student_assigned_project.keys():
        choice = student_project_permutation[student].index(student_assigned_project[student])

        print(student, choice)
        loss += 2**choice

    return loss



def find_best_distribution():
    # TODO
    pass



student_project_permutation = read_student_permutation_data()
student_list = [student for student in student_project_permutation.keys()]

popularity = make_project_popularity(student_project_permutation, display=True)


student_assigned_example = generate_random_distribution(student_list, student_project_permutation, True)

print("Loss for this example -> ", distribution_loss(student_assigned_example, student_project_permutation))