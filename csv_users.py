
import requests
import json
import time
import ast
import html2text
from bs4 import BeautifulSoup
import numpy
import csv


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Pick users from Dictionary

users_list = []

with open('canny_users.json', 'r') as f:
    content = f.read()
    users_canny = ast.literal_eval(content)

for value in users_canny.values():
    user_id = {
    "id": value
    }
    users_list.append(user_id)

    jprint(user_id)
    print(len(users_list))


# Get users from Canny API

endpoint_canny = "https://canny.io/api/v1/users/retrieve"

payload2 = {
'apiKey': '???'
}

headers = {
'Content-Type': 'application/json'
}

users_csv = []

for user in users_list:

    export_canny = requests.post(endpoint_canny, params=payload2, headers=headers, data=json.dumps(user))

    export_canny2 = export_canny.json()

    print(export_canny2)
    print(len(users_csv))

    users_csv.append(export_canny2)


# Create CSV

with open('csv_users.csv', mode='w') as users_list:
    users_writer = csv.writer(users_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for p in users_csv:
        users_writer.writerow([p["email"]])
