

def titleParser(text):
	import re
	text = re.sub("[^a-zA-Z0-9]+", " ",text)
	return text