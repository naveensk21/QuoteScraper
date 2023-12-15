import json
import random

with open('all_quotes.json', 'r') as fp:
    data = json.load(fp)

all_quotes = [quote['text'] for quote in data]
all_authors = [quote['author'] for quote in data]
random_quote = random.choice(all_quotes)
print(random_quote)

while guess.lower() != all_authors.lower():
    pass