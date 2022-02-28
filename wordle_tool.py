import re


#Scrape data
"""
import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

#url = 'http://www.allscrabblewords.com/5-letter-words/'
url="https://eslforums.com/5-letter-words/"
html = scraper.get(url).content

soup = BeautifulSoup(html, 'html.parser')
vals = soup.find_all('li')
my_list = []
for val in vals:
    my_list.append(val.text)
"""

def get_corpus():
    my_file = open("wordle-answers-alphabetical.txt", "r")
    content = my_file.read()
    corpus = content.split("\n")
    my_file.close()
    return corpus


def search_corpus(guesses, does_not_contain_list, does_contain_list
                 , re_not_like, re_like, corpus):
    matching = [word for word in corpus \
                    if not any(letter in word for letter in does_not_contain_list)
                    if not any(re.findall(exp, word) for exp in re_not_like)
                    if all(letter in word for letter in does_contain_list)
                    if re.findall(re_like, word)
                    ]
    return matching

def count_tokens(corpus, n):
    """
    Count based on a token length. 
    A Token lenght of 1 would count letters. 
    """
    result = {}
    for word in corpus:
    # Go through each letter in the text
        for i in range(0, len(word)-n+1, n):
            token = word[i:i+n]
        #for token in word
            # Check if the letter needs to be counted or not
            if token not in result:
                result[token] = 1
            # Add or increment the value in the dictionary
            else:
                result[token] += 1
    #sort dictionary
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return result


def get_re_like(guesses):
    """
    Return a regular expression for the correct letters
    """
    guess = list(guesses[-1][0])
    result = list(guesses[-1][1])
    re_like = list('.....')
    for element in range(len(guess)):
        if result[element] == 'g':
            re_like[element] = guess[element]
    re_like = "".join(re_like)
    return re_like


def get_re_not_like(guesses):
    """
    return a list of regular expressions that 
    are not like the answer
    """
    re_not_like =[]
    for guess in guesses:
        cur_guess= list(guess[0])
        cur_result = list(guess[1])
        for element in range(len(cur_guess)):
            if cur_result[element] == 'y':
                cur_re_not_like = list('.....')
                cur_re_not_like[element] = cur_guess[element]
                cur_re_not_like = "".join(cur_re_not_like)
                re_not_like.append(cur_re_not_like)
    return re_not_like


def get_does_contain(guesses):
    """
    get letters contained
    """
    does_contain =[]
    for guess in guesses:
        cur_guess= list(guess[0])
        cur_result = list(guess[1])
        for element in range(len(cur_guess)):
            if cur_result[element] == 'g' or cur_result[element] == 'y':
                does_contain.append(cur_guess[element])
    return does_contain


def get_does_not_contain (guesses):
    does_not_contain =[]
    for guess in guesses:
        cur_guess= list(guess[0])
        cur_result = list(guess[1])
        for element in range(len(cur_guess)):
            if cur_result[element] == 'b':
                does_not_contain.append(cur_guess[element])
    return does_not_contain


def main(guesses):
    does_contain_list =get_does_contain(guesses)
    re_not_like = get_re_not_like(guesses)
    re_like= get_re_like(guesses)
    does_not_contain_list= get_does_not_contain (guesses)
    corpus = get_corpus()

    matching = search_corpus(guesses, does_not_contain_list, does_contain_list
                 , re_not_like, re_like, corpus)
    print('*'*15)
    print(f'{len(matching)} words')
    print(matching)
    print(count_tokens(matching,1))
    print( '\n') 

guesses = [('tears', 'bybbb'), ('loves', 'bybyb'), ('opine', 'ybbbg')]
main(guesses)