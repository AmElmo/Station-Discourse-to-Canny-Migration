
# Migration of topics from the board "Bugs, support & troubleshooting"

import requests
import json
import csv
import time
import ast
import html2text

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

endpoint_slug = ["https://community.getstation.com/c/bugs/l/top/all.json"]

for f in endpoint_slug:
    i = 0
    while i < 10:

        payload1 = {
        "Api-Key": "???",
        "Api-Username": "julien"
        }

        parameters = {
        "page": i
        }


        list_slugs = requests.get(f, headers=payload1, params=parameters).json()

        if 'topic_list' not in list_slugs:
            break

        i = i + 1

        for d in list_slugs['topic_list']['topics']:
            # We only select topics that haven't be closed / merged
            if d['closed'] is not True:
                slug = d['slug']
                slugs_info.append(slug)

        jprint(slugs_info)
        print(len(slugs_info))


time.sleep(10)

# Get list of first posts

topic_slug = slugs_info

first_posts = []

for i in topic_slug:

    endpoint_topics = f"https://community.getstation.com/t/{i}.json"

    payload2 = {
    "Api-Key": "???",
    "Api-Username": "julien"
    }

    # paged_posts = requests.get(endpoint_topics, headers=payload2).json()['post_stream']['posts']

    topic = requests.get(endpoint_topics, headers=payload2).json()

    # Variables to extract (with topic + first post of the topic)

    with open('canny_users.json', 'r') as f:
        content = f.read()
        users_canny = ast.literal_eval(content)

    topic_info = {}
    for stream in topic['post_stream']['posts']:
        if stream['post_number'] == 1:
            topic_info = {
                "authorID":str(stream['user_id']),
                "created_at": stream['created_at']
            }

            break

    topic_info['title'] = h2t.handle(topic['fancy_title'])
    topic_info["cannyID"] = users_canny[topic_info['authorID']]

    first_posts.append(topic_info)

    # ???? topics_dictionary[info['discourseID']] = info['cannyID']

    # Ensure we don't hit the API rate limit
    time.sleep(2)

    jprint(topic_info)
    print(len(first_posts))

# # Create CSV list for topics
with open('topics_list_bugs2.csv', mode='w') as topic_list:
    fieldnames = ['Canny User ID', 'Title', 'Created At']
    topic_writer = csv.DictWriter(topic_list, fieldnames=fieldnames)
    topic_writer.writeheader()
    for p in first_posts:
        topic_writer.writerow({'Canny User ID': p['cannyID'], 'Title':p['title'], 'Created At': p['created_at']})
