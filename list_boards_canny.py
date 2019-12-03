
import requests
import json

endpoint_canny = "https://canny.io/api/v1/boards/list"

payload2 = {
'apiKey': '292eb22b-a1f2-cf73-d5a1-7ce005ffc4b2'
}

import_canny = requests.post(endpoint_canny, params=payload2)

###

print(import_canny.content)
