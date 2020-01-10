#!/usr/bin/env python3

import requests, json

# Il faut créer un fichier cookies.py, contenant les cookies dans un dico
# cookies = {
#   'name': 'value',
#   ...
# }
# Utilise editThisCookie, extention pour charger les cookies

from cookies import cookies

url = "https://evento.renater.fr/rest.php/question/219442/answer?format=json"

r = requests.get(url, cookies=cookies)

final_result = dict()

results = json.loads(r.content)

users = {}
users_answers = {}

for result in results:
    users[result["participant"]["name"]] = str(result["answer_id"])

for username in users.keys():
    users_answers[username] = json.loads(requests.get("https://evento.renater.fr/rest.php/answer/"+users[username], cookies=cookies).content)["comment"]


for student in users_answers.keys():
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


#print(final_result)

with open("data.txt", "w") as f:
    for student in final_result.keys():
        f.write("{}|{}\n".format(student, final_result[student]))