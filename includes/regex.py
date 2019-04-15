import re

get = re.compile("^(.*)\s*\=\s*\?\s*$", flags=re.IGNORECASE)

func = re.compile("(fun[a-z])\((\d+|[a-z]+)\)", flags=re.IGNORECASE)

evalFunc = re.compile("(fun[a-z])\(((?:[a-z]|[\d\s+\-\*\/\%])+)\)", flags=re.IGNORECASE)

draw = re.compile("draw\s*(fun[A-Z])", flags=re.IGNORECASE)

parseMatrice = re.compile("\[(\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)+)\]", flags=re.IGNORECASE)

put = re.compile("^\s*([A-Z]+|fun[A-Z]\([A-Z]\))\s*\=(.*)", flags=re.IGNORECASE)

checkMatrice = re.compile("(\[\[\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)+\](?:;\[\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)+\])*\])", flags=re.IGNORECASE)

checkLetter = re.compile("([A-Z])", flags=re.IGNORECASE)
