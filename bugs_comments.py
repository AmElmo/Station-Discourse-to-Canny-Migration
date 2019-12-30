
# Migration of comments from the board Bugs, support & troubleshooting Requests"

import requests
import json
import time
import ast
import html2text
from bs4 import BeautifulSoup
import numpy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process



def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Discourse sends HTML text for the topics and posts so we need to convert them to plain text for Canny
h2t = html2text.HTML2Text()

# We ignore images as they are sent to
h2t.ignore_images = True

# Get list of topic slugs to insert in the URL

slugs_info = []

i = 0

endpoint_slug = "https://community.getstation.com/c/bugs/l/top/all.json"

payload1 = {
"Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
"Api-Username": "julien"
}

parameters = {
"page": i
}

list_slugs = requests.get(endpoint_slug, headers=payload1, params=parameters).json()['topic_list']['topics']

for d in list_slugs:

    with open('canny_topics_bugs2.json', 'r') as p:
        content = p.read()
        topics_canny = ast.literal_eval(content)

    title2 = process.extractOne(d['title'], topics_canny.keys())
    print(title2)
    if title2[1] > 95:
        title3 = title2[0]
        print(title3)
    else:
        continue

    # We only select topics that haven't be closed / merged
    if (d['closed'] is not True and d['posts_count'] > 1):
        slug = f"{d['slug']}/{d['id']}"
        slugs_info.append(slug)

jprint(slugs_info)
print(len(slugs_info))

time.sleep(10)

# Get list of first posts

with open('canny_users.json', 'r') as f:
    content = f.read()
    users_canny = ast.literal_eval(content)

with open('canny_topics_bugs2.json', 'r') as p:
    content = p.read()
    topics_canny = ast.literal_eval(content)

topic_slug = ["1password-not-working-not-authenticating-wrong-credentials-cli-is-out-of-date/1930",
    "frequent-sign-outs-in-office-365-recurrent-logouts-in-microsoft-outlook-unable-to-sign-back-in-one-drive/1404",
    "cant-present-share-screen-in-skype-google-meet-hangouts-appear-in-stride-slack/683",
    "whatsapp-automatically-logs-out-qr-code-needs-to-be-scanned-again-after-quitting-exiting-station-leads-to-sign-outs/2874",
    "dropbox-keeps-showing-pop-up-window-collection-chooser-window-reopens-endlessly-on-closing-it/3077",
    "slack-messages-are-not-getting-marked-as-read-red-notification-dot-is-always-here/747",
    "cant-login-to-station-sso-2fa-not-supported-duo-onelogin-okta-rapididentity-google-titan-etc/2205",
    "notification-are-not-working-are-inconsistent-no-red-dots-activity-badges-on-the-apps-icons/2610",
    "skype-is-buggy-keeps-freezing-needs-frequent-reloading/4853",
    "app-store-is-stuck-blank-loading-applications-list-forever/2420",
    "wunderlist-is-not-working-displays-a-blank-screen/6343",
    "cant-install-station-undefined-error-setup-crashes/675",
    "full-white-blank-screen-upon-station-loading-startup/1407",
    "cant-logout-of-station-change-login-account-switch-login-email-address/2465",
    "station-cannot-detect-turned-off-do-not-disturb-mode-on-windows-focus-assist-is-always-on/3445",
    "how-to-uninstall-station/2915",
    "cant-launch-station-crashes-sqlite-error-duplicate-column-name-subdomain-manifesturl-alwaysloaded-installcontext/3143"]

first_posts = []

for i in topic_slug:
    top1 = process.extractOne(i, topics_canny.keys())
    print(top1)
    if top1[1] < 95:
        continue
    else:
        id = 1
        while id < 100:
            id = id + 1

            print(i)
            print(id)
            endpoint_topics = f"https://community.getstation.com/t/{i}/{id}.json"

            payload2 = {
            "Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
            "Api-Username": "julien"
            }

            # Ensure we don't hit the API rate limit
            time.sleep(1)

            topic = requests.get(endpoint_topics, headers=payload2).json()

            if 'posts_count' not in topic:
                continue

            if id > (topic['posts_count']+topic["reply_count"]+topic["reply_count"]):
                continue

            # Variables to extract (with topic + first post of the topic)

            topic_info = {}
            for stream in topic['post_stream']['posts']:
                if (stream['post_number'] == id and stream['cooked'] != ""):
                    topic_info = {
                        # "Topic ID":stream['topic_id'],
                        # "Created At":stream['created_at'],
                        "value":h2t.handle(stream['cooked']).replace("*", "").replace("_", ""),
                        "authorID":str(stream['user_id']),
                    }
                    topic_info['postID'] = topic['title']
                else:
                    continue

                    topic_info['imageURLs'] = []
                    imageURL = BeautifulSoup(stream['cooked'],'lxml').findAll('img')
                    for image_tag in imageURL:
                        if any(x in stream['cooked'] for x in ['/emoji/', '/user_avatar/']):
                            break
                        else:
                            if 'img src=\"https://' in stream['cooked']:
                                topic_info['imageURLs'].append(image_tag.get('src'))
                            else:
                                topic_info['imageURLs'].append(f"https://community.getstation.com{image_tag.get('src')}")


            first_posts.append(topic_info)

            jprint(topic_info)
            print(len(first_posts))


# Remove duplicates from pagination loop in the dictionary
first_posts_final = [i for n, i in enumerate(first_posts) if i not in first_posts[n + 1:]]

jprint(first_posts_final)
print(len(first_posts_final))

# Import data to Canny endpoint

endpoint_canny = "https://canny.io/api/v1/comments/create"

payload2 = {
'apiKey': '292eb22b-a1f2-cf73-d5a1-7ce005ffc4b2'
}

headers = {
'Content-Type': 'application/json'
}

count = 0
count2 = 0

    # Turn Discourse User IDs and Topics ID into Canny User and Topic IDs for linking existing data
for post in first_posts_final:
    userID = post['authorID']
    title1 = process.extractOne(post['postID'], topics_canny.keys())
    print(title1)
    if title1[1] > 97:
        title = title1[0]
    else:
        continue

    if userID not in users_canny:
        continue
    post['authorID'] = users_canny[userID]

    if title not in topics_canny:
        continue
    post['postID'] = topics_canny[title]

    import_canny = requests.post(endpoint_canny, params=payload2, headers=headers, data=json.dumps(post))

    print(post)

    print(import_canny.content)

    print(import_canny.status_code)

    count2 = count2+1
    print('progress: ' + str(count2))

    count = count+1
    print('count ' + str(count))
    if count == 3:
        print("sleeping")
        time.sleep(2)
        count = 0