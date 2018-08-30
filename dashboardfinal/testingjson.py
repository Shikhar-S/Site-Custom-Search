import requests
search_url = "http://127.0.0.1:8000/search/"
search_term = "hello"

import requests


params  = {"search_term": search_term,"crawler_id":28 ,"numres":5 }
response = requests.post(search_url,data=params)
# response.raise_for_status()
search_results = response.json()

print(search_results)


