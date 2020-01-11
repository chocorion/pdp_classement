#!/usr/bin/env python3

############################################################
#
#   Ce code repose sur le fait que peux de monde l'utilise.
#   Si je vous ai donné accés, merci de garder ça pour vous :)
#


import sys
from operator import itemgetter
from random import shuffle
from projects import projects


NUMBER_PROJECTS     = 25
GROUP_SIZE          = 5
DEFAULT_NUMBER_TRY  = 50000

def read_student_permutation_data(filename="data.txt"):
    ''' Read the permutation for each student, and return the dict '''

    file = open(filename, "r")
    lines = file.readlines()

    extracted_data = dict()

    for line in lines:
        if (line[0] == '#'):
            continue

        if ('|' not in line):
            continue

        (name, permutation) = line.split('|')
        permutation = permutation[1:(len(permutation) - 2)]
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


def display_distribution(distribution, student_list):
    ''' Display the distribution of student by project '''

    print('\n')
    for project_num in projects.keys():
        project_student_list = list()

        for student in student_list:
            if distribution[student] == project_num:
                project_student_list.append(student)

        print("{}.{:65s}\t -> {}".format(project_num, projects[project_num], project_student_list))
    print('\n')


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
        display_distribution(student_assigned_project, student_list)

    return student_assigned_project


    

def distribution_loss(student_assigned_project, student_project_permutation):
    ''' Compute distribution loss, based on what the prof say '''
    loss = 0

    for student in student_assigned_project.keys():
        choice = student_project_permutation[student].index(student_assigned_project[student])
        # loss += 2**choice
        loss += choice

    return loss



def print_progression_bar(max_number, current_number, current_loss, min_loss):
    ''' Display a beautiful progression bar for find_best_distribution '''

    progression = str(round((current_number/max_number) * 100, 2))

    print("Progression: {:4d}/{:4d} -> {:5s}% | Current loss -> {:6d} : Minimal loss -> {:6d}".format(current_number, max_number, progression, current_loss, min_loss), end='\n' if current_number == max_number else '\r')

    # \n at the end
    if current_number == max_number:
        print('\n')


def find_best_distribution(student_project_permutation, number_of_try, username, verbose=False):
    ''' The core algorithme, find best solution and make stats '''

    student_list = [student for student in student_project_permutation.keys()]
    stats = dict()
    
    best_assignement = generate_random_distribution(student_list, student_project_permutation)
    min_loss = distribution_loss(best_assignement, student_project_permutation)

    # for each loss, number of accurence and number of choice occurence
    stats[min_loss] = [1, [0 for i in range(NUMBER_PROJECTS)]]


    for i in range(1, number_of_try):
        current_assignement = generate_random_distribution(student_list, student_project_permutation)
        current_loss = distribution_loss(current_assignement, student_project_permutation)

        if current_loss in stats.keys():
            stats[current_loss][0] += 1
        else:
            stats[current_loss] = [1, [0 for i in range(NUMBER_PROJECTS)]]

        if verbose:
            # +1 because 1 already used for initialisation, 
            print_progression_bar(number_of_try, i + 1, current_loss, min_loss)

        if current_loss < min_loss:
            min_loss = current_loss
            best_assignement = current_assignement


        choice_position = student_project_permutation[username].index(current_assignement[username])
        stats[current_loss][1][choice_position] += 1


    if (verbose):
        loss_list = [i for i in stats.keys()]
        loss_list.sort()

        print("Your firsts projects : ")

        
        for i in range(4):
            print("\t{}. {}".format(i + 1, projects[student_project_permutation[username][i]]))

        print("\n\nLoss frequency : Chance to have project")
        
        for i in loss_list:
            print("{:10d} -> {:10d} ({:6s}%) {}".format(i,stats[i][0],str(round((stats[i][0]/number_of_try)*100, 2)), [round((j/stats[i][0]) * 100, 2) for j in stats[i][1]]))

    return best_assignement


def usage():
    print("\nUsage :")
    print("\t./main.py <number_of_try (opt)> <\"your_name\" (opt)>")




if __name__ == "__main__":
    username = ""
    if len(sys.argv) == 2:
        try:
            number_try = int(sys.argv[1])
        except:
            usage()
            sys.exit(0)

    elif len(sys.argv) == 3:
        try:
            number_try = int(sys.argv[1])
            username = sys.argv[2]
        except:
            usage()
            sys.exit(0)
    elif len(sys.argv) == 4:
        print("Put your name between \"\" please, i'm lazy...")
        usage()

        sys.exit(0)
    else:
        number_try = DEFAULT_NUMBER_TRY


    student_project_permutation = read_student_permutation_data()
    student_list = [student for student in student_project_permutation.keys()]

    if username != "" and username not in student_list:
        print("Error, {} not in student list...".format(username))
        print("Student list -> ")
        for student in student_list:
            print("\t", student)

        print("Please, use juste the name displayed without any extra space, i don't like string manipulation...")

        sys.exit(0)

    elif username == "":
        unsername_find = False
        target_find = False
        print ("What is your name ?")
        for i in range(len(student_list)):
            print("\t{} -> {}".format(i, student_list[i]))

        while not unsername_find:
            try:
                num = int(input("Enter student num : "))
            except:
                print("You must enter a number !")
            
            if num >= len(student_list) or num < 0:
                print("Number not in range, are you idiot ?")
            
            username = student_list[num]
            unsername_find = True

        #Just display project
        print('\n')
        for num in projects.keys():
            print("{}.{}".format(num, projects[num]))
        print('\n')

        while not target_find:
            try:
                num = int(input("Enter the target project number : "))
            except:
                print("You must enter a number !")
            
            if num > 25 or num < 1:
                print("Number not in range, are you idiot ?")
            
            target = num
            target_find = True



    print("\n\nHello {} !".format(username))
    print("Current number of students in database -> {}\n\n".format(len(student_list)))

    popularity = make_project_popularity(student_project_permutation, display=True)

    sortedPop = sorted(popularity.items(),key=lambda e: e[1][(24)])
    
    for s in range(0,24):
        sortedPop = sorted(sortedPop,key=lambda e: e[1][(23-s)])

    if (True):
        print("\tProject popularity sorted :\n\n")
        for (project_num,pops) in sortedPop:
            print("{}.{:65s}\t{}".format(project_num, projects[project_num], pops))
        print('\n\n')

    student_project_permutation[username][0] = target
    slot = 1
    for s in range(0,25):
        if sortedPop[(24-s)][0] == target or slot > 24:
            continue

        student_project_permutation[username][slot] = sortedPop[(24-s)][0]
        slot += 1
    
    print("Choix : ")
    print(student_project_permutation[username])

    best_assignement = find_best_distribution(student_project_permutation, number_try, username, verbose=True)

    print("\n\nExemple de distribution :")
    display_distribution(best_assignement, [student for student in student_project_permutation.keys()])
