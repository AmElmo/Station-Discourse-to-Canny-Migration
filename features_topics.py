
# Migration of topics from the board "Feature Requests""

import requests
import json
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

# Get list of topic slugs to insert in the URL

slugs_info = []

i = 0
while i < 3:
    i = i + 1

    endpoint_slug = "https://community.getstation.com/c/features-request/l/top/all.json"

    payload1 = {
    "Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
    "Api-Username": "julien"
    }

    parameters = {
    "page": i
    }

    list_slugs = requests.get(endpoint_slug, headers=payload1, params=parameters).json()['topic_list']['topics']

    for d in list_slugs:
        # We only select topics that haven't be closed / merged
        if d['closed'] is not True:
            slug = d['slug']
            slugs_info.append(slug)

    jprint(slugs_info)
    print(len(slugs_info))

    nb_topics_exported = len(slugs_info)

    if nb_topics_exported == 0:
        break

# Get list of first posts

topic_slug = ["paste-and-match-style/8923"]

first_posts = []

for i in topic_slug:

    endpoint_topics = f"https://community.getstation.com/t/{i}.json"

    payload2 = {
    "Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
    "Api-Username": "julien"
    }

    # paged_posts = requests.get(endpoint_topics, headers=payload2).json()['post_stream']['posts']

    topic = requests.get(endpoint_topics, headers=payload2).json()

    # Variables to extract (with topic + first post of the topic)

    topic_info = {}
    for stream in topic['post_stream']['posts']:
        if stream['post_number'] == 1:
            topic_info = {
                # "Topic ID":stream['topic_id'],
                # "Created At":stream['created_at'],
                "details":h2t.handle(stream['cooked']).replace("*", "").replace("_", ""),
                "authorID":str(stream['user_id']),
                "topic_id": stream['topic_id']
            }
            # Ensure we don't hit the API rate limit
            time.sleep(2)

            break

    topic_info['title'] = h2t.handle(topic['fancy_title'])
    topic_info["boardID"] = '5dea64c138114a41847c0787'
    if topic['image_url'] is not None:
        topic_info['imageURLs'] = topic['image_url'].split(',')

    first_posts.append(topic_info)

    jprint(topic_info)
    print(len(first_posts))


# Import data to Canny endpoint

# Create dictionary for topics
topics_dictionary = {}

endpoint_canny = "https://station.canny.io/api/v1/posts/create"

payload2 = {
'apiKey': '292eb22b-a1f2-cf73-d5a1-7ce005ffc4b2'
}

headers = {
'Content-Type': 'application/json'
}

count = 0

with open('canny_users.json', 'r') as f:
    content = f.read()
    users_canny = ast.literal_eval(content)

    # ?? Add dictionary here

for post in first_posts:
    userID = post['authorID']
    if userID not in users_canny:
        continue
    post['authorID'] = users_canny[userID]

    # Remove the "topic_id" not needed with Canny API
    new_post = {key:val for key, val in post.items() if key != 'topic_id'}

    import_canny = requests.post(endpoint_canny, params=payload2, headers=headers, data=json.dumps(new_post))

    print(post)

    print(import_canny.content)

    print(import_canny.status_code)

    #Push data into dictionary

    import_canny2 = import_canny.json()

    info = {
        "discourseID":post['topic_id'],
        "cannyID":import_canny2['id']
    }

    print(import_canny2['id'])

    topics_dictionary[info['discourseID']] = info['cannyID']

    count = count+1
    print('count ' + str(count))
    if count == 3:
        print("sleeping")
        time.sleep(2)
        count = 0

# Create JSON dictionary for topics
with open('canny_topics_features.json', 'w') as fp:
    json.dump(topics_dictionary, fp)
