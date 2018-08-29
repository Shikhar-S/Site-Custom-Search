subkey='dcf13da58d784c3ab9bc479dcdd55e8a'
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
search_term = "Azure Cognitive Services"

import requests

headers = {"Ocp-Apim-Subscription-Key" : subkey}
params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

print(search_results['webPages']['value'][0:])


