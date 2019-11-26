
import requests
import json

# Get list of users

users = []

i = 0
while i < 4:
    i = i + 1

    endpoint_users = "https://community.getstation.com/admin/users/list/active.json?show_emails=true"

    payload = {
    "Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
    "Api-Username": "julien"
    }

    parameters = {
    "page": i
    }

    paged_users = requests.get(endpoint_users, headers=payload, params=parameters).json()

    users.append(paged_users)

    # Specific variables to extract
    users_info = []
    for d in paged_users:
        info = {
        "userID":d['id'],
        "name":d['name'],
        "username":d['username'],
        "email":d['email'],
        "created":d['created_at'],
        "avatarURL":"https://community.getstation.com" + d['avatar_template'].replace("{size}", "240")
        }
        users_info.append(info)

# create a formatted string of the JSON object
        def jprint(obj):
            text = json.dumps(obj, sort_keys=True, indent=4)
            print(text)

        #jprint(users_info)

        jprint(users_info)

print(len(users))

# import data to Canny endpoint

endpoint_canny = "https://station.canny.io/api/v1/users/find_or_create"

payload2 = {
'apiKey': "292eb22b-a1f2-cf73-d5a1-7ce005ffc4b2"
}

my_data = {
"avatarURL": "https://community.getstation.com/user_avatar/community.getstation.com/julien/240/66_2.png",
"created": "2017-10-20T04:27:45.769Z",
"email": "julien@getstation.com",
"name": "Julien Berthomier",
"userID": 13,
"username": "julien"
}

import_canny = requests.post(endpoint_canny, data=my_data, params=payload2)

print(import_canny.status_code)
