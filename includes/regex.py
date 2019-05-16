import re

get = re.compile("^(.*)\s*=\s*\?\s*$", flags=re.IGNORECASE)

put = re.compile("^\s*([A-Z]+|fun[A-Z]\([A-Z]\))\s*=(.*)", flags=re.IGNORECASE)

reset = re.compile("^\s*reset\s*(.*)\s*$", flags=re.IGNORECASE)

complex = re.compile("(?:(\d+)\s*)?([+\-]?\s*\d+)\s*\*?\s*i", flags=re.IGNORECASE)

func = re.compile("(fun[a-z])\((\d+|[a-z]+)\)", flags=re.IGNORECASE)

evalFunc = re.compile("(fun[a-z])\(((?:[a-z]|[\d\s+\-*/%])+)\)", flags=re.IGNORECASE)

draw = re.compile("^\s*draw\s*(fun[A-Z])\s*", flags=re.IGNORECASE)

checkMatrice = re.compile("(\[\[\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)*\](?:;\[\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)*\])*\])", flags=re.IGNORECASE)

parseMatrice = re.compile("\[(\d+(?:\.\d+)?(?:,\d+(?:\.\d+)?)*)\]", flags=re.IGNORECASE)

checkLetter = re.compile("([A-HJ-Z])", flags=re.IGNORECASE)





