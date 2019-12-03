
# Need to be filtered by "poster":d['posters'], "description": "Original Poster


import requests
import json

# Get list of topics

topics = []

i = 1
while i < 2:
    i = i + 1

    endpoint_topics = "https://community.getstation.com/c/ux-design/l/top/all.json"

    payload = {
    "Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
    "Api-Username": "julien"
    }

    parameters = {
    "page": i
    }

    paged_topics = requests.get(endpoint_topics, headers=payload, params=parameters).json()['topic_list']['topics']

    topics.append(paged_topics)


    # Variables to extract
    topics_info = []
    for d in paged_topics:
        if d['closed'] is not True:
            info = {
            "id":d['id'],
            "title":d['title'],
            "image_url":d['image_url'],
            "poster":d['posters'],
            "views":d['views'],
            "likes":d['like_count'],
            "vote_count":d['vote_count'],
            "created_at":d['created_at'],
            }
            topics_info.append(info)


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(topics_info)

print(len(topics))



# Open as JSON file
# with open('data.json', 'w') as fp:
    # json.dump(paged_topics, fp)
