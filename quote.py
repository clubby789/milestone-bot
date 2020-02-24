import requests
import json
def getQuote():
	try:
		url = "https://inspirobot.me/api?generateFlow=1"
		r = requests.get(url)

		quote = json.loads(r.text)['data'][1]['text']
	except:
		quote = -1
	return quote
