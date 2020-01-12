#!/usr/bin/env python3

############################################################
#
#   Ce code repose sur le fait que peux de monde l'utilise.
#   Si je vous ai donné accés, merci de garder ça pour vous :)
#


import sys
from random import shuffle
from projects import projects

DEFAULT_NUMBER_TRY  = 50000

class Student:
    def __init__(self, name, permutation):
        self.name = name
        self.permutation = permutation

    def get_choice_number(self, choice_number):
        return self.permutation[choice_number]

    def get_project_position(self, project_num):
        return self.permutation.index(project_num)


class PdP:
    def __init__(self):
        self.number_of_projects = 25
        self.group_size = 5
        self.number_of_student = 0

        self.student_list = list()

        self.projects = projects
        self.projects_keys = self.projects.keys()


    
    def add_student(self, student):
        self.student_list.append(student)
        self.number_of_student += 1


    def get_student_by_index(self, index):
        return self.student_list[index]
    
    def add_student_from_db(self, filename="data.txt"):
        with open(filename, "r") as file:
            for line in file.readlines():

                # Empty line or comment
                if line[0] == '#' or '|' not in line:
                    continue

                (name, permutation) = line.split('|')
                permutation = permutation[1:len(permutation) - 2] # Remove [, ] and \n

                self.add_student(Student(name, [int(i) for i in permutation.split(',')]))


    def print_project_popularity(self):
        project_popularity = dict()

        for projects_key in self.projects_keys:
            project_popularity[projects_key] = [0 for i in range(self.number_of_projects)]

        for student in self.student_list:
            for i in range(self.number_of_projects):
                student_ieme_choice = student.get_choice_number(i)

                project_popularity[student_ieme_choice][i] += 1

        print("\tProject popularity :\n\n")

        for projects_key in self.projects_keys:
            print("{}.{:65s}\t{}".format(projects_key, self.projects[projects_key], project_popularity[projects_key]))


class Project_distribution:
    def __init__(self, pdp):
        self.pdp = pdp
        self.distribution = dict()

        for student in pdp.student_list:
            self.distribution[student] = list()


    @staticmethod
    def generate_random(pdp):
        random_permutation = [i for i in range(pdp.number_of_student)]
        shuffle(random_permutation)

        project_distribution = Project_distribution(pdp)

        project_occupation = dict()

        for projects_key in pdp.projects_keys:
            project_occupation[projects_key] = 0

        
        for student_index in random_permutation:
            student = pdp.get_student_by_index(student_index)

            for project_position in range(pdp.number_of_projects):
                student_choice = student.get_choice_number(project_position)

                if project_occupation[student_choice] < pdp.group_size:
                    project_occupation[student_choice] += 1

                    project_distribution.distribution[student] = student_choice
                    break
            else:
                print("Error, student without project in distribution...")
                sys.exit(0)

        return project_distribution


    def loss(self):
        loss = 0

        for student in self.pdp.student_list:
            assigned_project = self.distribution[student]
            choice = student.get_project_position(assigned_project)

            # Si linéaire
            loss += choice

            #Sinon, quelque chose comme
            # loss += 2**choice

        return loss


    def print_distribution(self):
        for projects_key in pdp.projects_keys:
            student_assigned = list()

            for student in pdp.student_list:
                if self.distribution[student] == projects_key:
                    student_assigned.append(student)
            
            print("{}.{:65s}\t -> {}".format(projects_key, pdp.projects[projects_key], student_assigned))


    @staticmethod
    def print_progress_bar(max_try, current_try_number):
        progression = str(round((current_try_number/max_try) * 100, 2))

        print(
            "Progression: {:4d}/{:4d} -> {:5s}%".format(current_try_number, max_try, progression),
            end='\n' if current_try_number == max_try else '\r'
        )


    @staticmethod
    def get_bests_distributions_on_n_try(pdp, n):
        distributions = dict()

        for i in range(n):
            distribution = Project_distribution.generate_random(pdp)
            loss = distribution.loss()

            if loss in distributions.keys():
                distributions[loss].append(distribution)
            else:
                distributions[loss] = [distribution]
            
            Project_distribution.print_progress_bar(n, i + 1)

        best_loss = min(distributions.keys())

        return distributions[best_loss]
        

    @staticmethod
    def display_group_probability(pdp, distributions):
        number_of_distributions = len(distributions)

        project_repartition = dict()

        for projects_key in pdp.projects_keys:
            project_repartition[projects_key] = dict()

        
        for distribution in distributions:
            for student in pdp.student_list:
                assigned_project = distribution.distribution[student]

                if student in project_repartition[assigned_project]:
                    project_repartition[assigned_project][student] += 1
                else:
                    project_repartition[assigned_project][student] = 1

        
        for projects_key in pdp.projects_keys:
            print("{}.{}\n".format(projects_key, pdp.projects[projects_key]))

            for student in project_repartition[projects_key]:
                proba = (project_repartition[projects_key][student]/number_of_distributions) * 100
                proba = round(proba, 2)

                print("\t{:20s}".format(student.name), end='')
                print(" ({:6s} %)".format(str(proba)))
            
            print('')



if __name__ =="__main__":
    number_try = DEFAULT_NUMBER_TRY

    if len(sys.argv) == 2:
        try:
            number_try = int(sys.argv[1])
        except:
            print('./rewrite.py <number_of_try (optionnal)>')
            sys.exit(0)

    pdp = PdP()
    pdp.add_student_from_db()
    pdp.print_project_popularity()

    best_distributions = Project_distribution.get_bests_distributions_on_n_try(pdp, number_try)
    Project_distribution.display_group_probability(pdp, best_distributions)