import requests
def getQuote():
	try:
		r = requests.get("http://inspirobot.me/api?generate=true")
		quote = r.text
	except:
		return -1
	if quote.startswith("https://generated.inspirobot.me/a/"):
		return quote
	return -1