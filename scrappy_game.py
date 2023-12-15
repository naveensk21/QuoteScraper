import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
pd.options.display.width = 0

base_url = 'https://quotes.toscrape.com'

# load the dataset
with open('all_quotes.json', 'r') as fp:
    data = json.load(fp)

# get all the quotes
quotes = [i['text'] for i in data]


# check if the user answer matches
def check(random_value):
    for quote in data:
        if quote['text'] == random_value:
            return quote['author'].lower()


# extract the bio of the author
def hints(random_value):
    description = []
    for quote in data:
        if quote['text'] == random_value:
            res = requests.get(f'{base_url}{quote["about_link"]}')
            soup = BeautifulSoup(res.text, 'html.parser')
            description.append({"author_name": soup.find(class_="author-title").get_text(),
                                "author_dob": soup.find(class_="author-born-date").get_text(),
                                "author_born_location": soup.find(class_="author-born-location").get_text(),
                                "author_description": soup.find(class_="author-description").get_text()
                                })
    return description


# get the bio of the particular author
def get_quote_hints(random_value):
    hint_data = hints(random_value)
    return hint_data


# initiate to play the game again
def play_again(random_value):
    again = ' '
    while again not in ('yes', 'y', 'no', 'n'):
        again = input("Would you like to play again? Enter 'y / n': ")
    if again.lower() in ('yes', 'y'):
        return play(random_value)
    else:
        print("Goodbye ! Thanks for playing !")


# initiate to play the game
def play(quotes_list):
    num_guess = 4
    random_quote = random.choice(quotes_list)
    while num_guess > 0:
        print(f'Number of Guesses: {num_guess}')
        print("Guess the quote: ")
        print(random_quote)
        hint_data = get_quote_hints(random_quote)

        user_input = input("Who said this quote: ")
        if user_input.lower() == check(random_quote):
            print("You guessed correctly")
            break
        num_guess -= 1
        if num_guess == 3:
            print(" ")
            print(f"Here's a Hint: The author was born on {hint_data[0]['author_dob']} {hint_data[0]['author_born_location']}")
        elif num_guess == 2:
            print(" ")
            print(f"Here's another Hint: Authors first name initial is {hint_data[0]['author_name'][0]}")
        elif num_guess == 1:
            print(" ")
            last_name = hint_data[0]['author_name'].split()[1][0]
            print(f"Here's another Hint: Authors next/last initial is {last_name}")
        elif num_guess == 0:
            print("You ran out of guesses !!!")
            print(f'The answer is: {hint_data[0]["author_name"]}')
            return play_again(random_quote)


if __name__ == "__main__":
    play(quotes)






