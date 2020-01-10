#!/usr/bin/env python3

import requests, json

from cookies import cookies

url = "https://evento.renater.fr/rest.php/question/219442/answer?format=json"

r = requests.get(url, cookies=cookies)


results = json.loads(r.content)

users = {}
users_answers = {}

for result in results:
    users[result["participant"]["name"]] = str(result["answer_id"])

for username in users.keys():
    users_answers[username] = json.loads(requests.get("https://evento.renater.fr/rest.php/answer/"+users[username], cookies=cookies).content)["comment"]

print(users_answers) 