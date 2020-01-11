#!/usr/bin/env python3

import requests, json

# Il faut remplacer le contenu d'exemple de cookies.txt 
# par ce qu'on obtient en exportant les cookies depuis l'extension EditThisCookie sur chrome

from getcookies import getcookies

cookies = getcookies()

FULL_CSV = False

url = "https://evento.renater.fr/rest.php/question/219442/answer?format=json"

r = requests.get(url, cookies=cookies)

final_result = dict()
getcookies
results = json.loads(r.content)

users = {}
users_answers = {}

for result in results:
    users[result["participant"]["name"]] = str(result["answer_id"])

number_student = len(users.keys())
print("Downloading {} comments...".format(number_student))
count = 0
for username in users.keys():
    users_answers[username] = json.loads(requests.get("https://evento.renater.fr/rest.php/answer/"+users[username], cookies=cookies).content)["comment"]
    count += 1

    print("{}/{}\t{:20s} -> {}".format(count, number_student,username, users_answers[username]))
    
print("Done !")

for student in users_answers.keys():
    if FULL_CSV:
        final_result[student] = users_answers[student]
        continue

    student_choice = list()

    try:
        test_array = [0 for i in range(25)]
        user_choice_string = users_answers[student].split(',')

        if len(user_choice_string) != 25:
            continue
        
        for number in user_choice_string:
            if int(number) < 1 or int(number) > 25:
                raise Exception()

            test_array[int(number) - 1] += 1

            if test_array[int(number) - 1] == 2:
                raise Exception()

            student_choice.append(int(number))

    except:
        continue

    final_result[student] = student_choice
   

print("Number of correct answer : ", len(final_result.keys()))

with open("data.txt", "w") as f:
    for student in final_result.keys():
        if not FULL_CSV:
            f.write("{}|{}\n".format(student, final_result[student]))
        else:
            f.write("{},\"{}\"\n".format(student, str(final_result[student]).replace('.','').replace('\n','')))