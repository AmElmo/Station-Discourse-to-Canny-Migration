
# Need to be filtered by "poster":d['posters'], "description": "Original Poster


import requests
import json

# Get list of topics

endpoint_posts = "https://community.getstation.com/c/ux-design/l/top/all.json"

payload = {
"Api-Key": "e6242d57ec00311031cb8494eed3d8c11bcbba83fc4c9242194322b281ca8ff2",
"Api-Username": "julien"
}

paged_posts = requests.get(endpoint_posts, headers=payload).json()['topic_list']['topics']

# Variables to extract
posts_info = []
for d in paged_posts:
        info = {
        "title":d['title'],
        "imageURLs":d['image_url'],
        "boardID": "5d9a15a669f7170bf64e3bed",
        "poster":d['posters'],
        "created_at":d['created_at'],
        }
        posts_info.append(info)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(posts_info)

print(len(posts_info))



# Open as JSON file
# with open('data.json', 'w') as fp:
    # json.dump(paged_topics, fp)
