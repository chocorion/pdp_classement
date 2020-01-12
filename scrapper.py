#!/usr/bin/env python3

import requests, json

# Il faut remplacer le contenu d'exemple de cookies.txt 
# par ce qu'on obtient en exportant les cookies depuis l'extension EditThisCookie sur chrome

from getcookies import getcookies

cookies = getcookies()

EXPORT_CSV = True

url = "https://evento.renater.fr/rest.php/question/219442/answer?format=json"

r = requests.get(url, cookies=cookies)

final_result = dict()
full_result = dict()
getcookies
results = json.loads(r.content)

users = {}
users_answers = {}

try:
    for result in results:
        users[result["participant"]["name"]] = str(result["answer_id"])
except:
    print("Failed to parse results, did your cookies expire ?")
    exit()

number_student = len(users.keys())
print("Downloading {} comments...".format(number_student))
count = 0
for username in users.keys():
    users_answers[username] = json.loads(requests.get("https://evento.renater.fr/rest.php/answer/"+users[username], cookies=cookies).content)["comment"]
    count += 1

    print("{}/{}\t{:20s} -> {}".format(count, number_student,username, users_answers[username]))
    
print("Done !")

for student in users_answers.keys():

    student_choice = list()

    try:
        test_array = [0 for i in range(25)]
        user_choice_string = users_answers[student].split(',')

        if len(user_choice_string) != 25:
            raise Exception()
        
        for number in user_choice_string:
            if int(number) < 1 or int(number) > 25:
                raise Exception()

            test_array[int(number) - 1] += 1

            if test_array[int(number) - 1] == 2:
                raise Exception()

            student_choice.append(int(number))

    except:
        if EXPORT_CSV:
            full_result[("err:"+str(student))] = users_answers[student]
        continue

    full_result[student] = student_choice

for s in [s for s in full_result.keys() if not s.startswith("err:")]:
    final_result[s] = full_result[s]

print("Number of correct answer : ", len(final_result))

datas = dict()
try:
    file = open("data.txt", "r")
except:
    print("No database found...")
else:
    lines = file.readlines()

    for line in lines:
        (name, permutation) = line.split('|')
        datas[name] = permutation

    file.close()

with open("data.txt", "w") as f:
    for student in final_result.keys():
        if student in datas.keys():
            # print(datas[student][0:len(datas[student]) - 1], str(final_result[student]))
            if datas[student][0:len(datas[student]) - 1] != str(final_result[student]):
                print("{} replace {} with {} !".format(student, datas[student], final_result[student]))
        else:
            print("New student, {} -> {}".format(student, final_result[student]))

        f.write("{}|{}\n".format(student, final_result[student]))

if EXPORT_CSV:
    with open("data.csv", "w") as f:
        for student in full_result.keys():
            v = full_result[student]
            
            try:
                if type(full_result[student]) == list:
                    v = ",".join(str(n) for n in full_result[student])
            except:
                pass
            f.write("{},\"{}\"\n".format(student, v))
