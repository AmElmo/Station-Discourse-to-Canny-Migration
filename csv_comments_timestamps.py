
# Migration of topics from the board "Bugs, support & troubleshooting"

import requests
import json
import csv
import time
import ast
import html2text
import numpy


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Discourse sends HTML text for the topics and posts so we need to convert them to plain text for Canny
h2t = html2text.HTML2Text()

# We ignore images as they are sent to
h2t.ignore_images = True
h2t.ignore_bold = True
h2t.ignore_italic = True

# Get list of topic slugs to insert in the URL

slugs_info = []


i = 0
while i < 10:
    print(i)

    endpoint_slug = "https://community.getstation.com/c/bugs/l/top/all.json"

    payload1 = {
    "Api-Key": "???",
    "Api-Username": "julien"
    }

    parameters = {
    "page": i
    }

    list_slugs = requests.get(endpoint_slug, headers=payload1, params=parameters).json()

    i = i + 1

    for d in list_slugs['topic_list']['topics']:

        # We only select topics that haven't been closed / merged
        if (d['closed'] is not True and d['posts_count'] > 1):
            slug = f"{d['slug']}/{d['id']}"
            slugs_info.append(slug)



        jprint(slugs_info)
        print(len(slugs_info))


time.sleep(10)

# Get list of first posts


topic_slug = slugs_info

all_comments = []

for i in topic_slug:

    with open('canny_users.json', 'r') as f:
        content = f.read()
        users_canny = ast.literal_eval(content)

    id = 1
    while id < 100:
        id = id + 1

        print(i)
        print(id)
        endpoint_topics = f"https://community.getstation.com/t/{i}/{id}.json"

        payload2 = {
        "Api-Key": "???",
        "Api-Username": "julien"
        }

        # Ensure we don't hit the API rate limit
        time.sleep(1)

        topic = requests.get(endpoint_topics, headers=payload2).json()

        if 'posts_count' not in topic:
            break

        if id > (topic['posts_count']+topic["reply_count"]+topic["reply_count"]):
            break

        # Variables to extract for each comment

        topic_info = {}
        for stream in topic['post_stream']['posts']:
            if (stream['post_number'] == id and stream['cooked'] != ""):
                topic_info = {
                    # "Topic ID":stream['topic_id'],
                    # "Created At":stream['created_at'],
                    "comment":h2t.handle(stream['cooked']).replace("*", "").replace("_", ""),
                    "authorID":str(stream['user_id']),
                    "created_at": stream['created_at']
                }
                topic_info['title'] = h2t.handle(topic['fancy_title'])

                if topic_info['authorID'] in users_canny:
                    topic_info["cannyID"] = users_canny[topic_info['authorID']]
                else:
                    topic_info["cannyID"] = topic_info['authorID']

                all_comments.append(topic_info)

                jprint(topic_info)
                print(len(all_comments))



# Remove duplicates from list
all_comments_final = [i for n, i in enumerate(all_comments) if i not in all_comments[n + 1:]]

jprint(all_comments_final)

# # Create CSV list for topics
with open('comments_list_bugs2.csv', mode='w') as topic_list:
    fieldnames = ['Canny User ID', 'Topic Title', 'Comment', 'Created At']
    topic_writer = csv.DictWriter(topic_list, fieldnames=fieldnames)
    topic_writer.writeheader()
    for p in all_comments_final:
        topic_writer.writerow({'Canny User ID': p['cannyID'], 'Topic Title': p['title'], 'Comment': p['comment'], 'Created At': p['created_at']})
