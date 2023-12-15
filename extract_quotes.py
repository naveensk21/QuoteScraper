import json

import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import csv

all_quotes = []
base_url = 'https://quotes.toscrape.com'
page_url = '/page/1/'

while page_url:
    res = requests.get(f'{base_url}{page_url}')
    print(f"Scarping {base_url}{page_url}...")
    soup = BeautifulSoup(res.text, "html.parser")
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        quote_txt = quote.find(class_='text').get_text()
        quote_author = quote.find(class_='author').get_text()
        quote_about = quote.find('a')['href']
        quote_tag = quote.find('meta')['content']

        all_quotes.append({
            "text": quote_txt,
            "author":quote_author,
            "about_link":quote_about,
            "tags": quote_tag
        })

    next_btn = soup.find(class_='next')
    page_url = next_btn.find('a')['href'] if next_btn else None
    # each time it loops it will wait 2 seconds before requesting again
    # sleep(2)


# save extracted data to a csv file
# field_names = ['text', 'author', 'about_link', 'tags']
#
# with open('all_quotes_new.csv', 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=field_names)
#     writer.writeheader()
#     writer.writerows(all_quotes)
# df = pd.DataFrame(all_quotes)
# df.to_csv('all_quotes.csv')

# save to json
with open('all_quotes.json', 'w') as fp:
    json.dump(all_quotes, fp)