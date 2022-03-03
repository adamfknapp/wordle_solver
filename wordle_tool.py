import re

def get_corpus():
    """
    Get the corpus of valid words
    """
    my_file = open("wordle-answers-alphabetical.txt", "r")
    content = my_file.read()
    corpus = content.split("\n")
    my_file.close()
    return corpus


def search_corpus(does_not_contain_list, does_contain_list
                 , re_not_like, re_like, corpus):
    """
    Search the corpus for conditions
    """
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
    re_like = '.....'
    for guess in guesses:
        cur_guess= list(guess[0])
        cur_result = list(guess[1])
        #convert string to list
        re_like_lst =list(re_like)
        for element in range(len(cur_guess)):
            if cur_result[element] == 'g':
               re_like_lst[element] = cur_guess[element]
        #convert list to string
        re_like = "".join(re_like_lst)  
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


def contains(guesses, does_contain=True):
    """
    get letters contained or not contined
    True:  Does contain letters
    False: Does NOT contain letters
    """
    res =[]
    for guess in guesses:
        cur_guess= list(guess[0])
        cur_result = list(guess[1])
        for element in range(len(cur_guess)):
            if does_contain: 
                if cur_result[element] != 'b':
                    res.append(cur_guess[element])
            else:
                if cur_result[element] == 'b':
                    res.append(cur_guess[element])              
    return list(set(res))


def main(guesses):
    """
    Orchastrate result and ouput results
    """
    does_contain_list =contains(guesses, does_contain=True)
    print(does_contain_list)

    re_not_like = get_re_not_like(guesses)
    print(re_not_like)

    re_like= get_re_like(guesses)
    print(re_like)

    does_not_contain_list= contains (guesses, does_contain=False)
    print(does_not_contain_list)

    corpus = get_corpus()
    matching = search_corpus(does_not_contain_list, does_contain_list
                , re_not_like, re_like, corpus)
    tokens = count_tokens(matching,1)

    # Print results
    print('*'*15)
    print(f'{len(matching)} words')
    print(matching)
    print(tokens)
    print( '\n') 

guesses = [ ('crane', 'bybby'),
            ('carve', 'bbyby'),
            ('ovine', 'bbbby'),
            ('alter', 'bbggg'),
            ('shear', 'bbybg'),
            ('smear', 'byybg')
            ]
main(guesses)