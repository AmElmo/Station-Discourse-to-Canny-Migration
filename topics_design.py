

import requests
import json
import time

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Get list of topic slugs to insert in the URL

endpoint_slug = "https://community.getstation.com/c/ux-design/l/top/all.json"

payload1 = {
"Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
"Api-Username": "julien"
}

list_slugs = requests.get(endpoint_slug, headers=payload1).json()['topic_list']['topics']

slugs_info = []
for d in list_slugs:
    # We only select topics that haven't be closed
    if d['closed'] is not True:
        slug = d['slug']
        slugs_info.append(slug)

jprint(slugs_info)

# Get list of first posts

topic_slug = slugs_info

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
                "Topic ID":stream['topic_id'],
                "Created At":stream['created_at'],
                "Text":stream['cooked'],
                "User ID":stream['user_id']
            }
            # Ensure we don't hit the API rate limit
            time.sleep(2)

            break

    topic_info['Title'] = topic['fancy_title']
    topic_info['imageURLs'] = topic['image_url']

    first_posts.append(topic_info)

    jprint(topic_info)

print(len(topic))
