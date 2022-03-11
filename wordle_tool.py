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


def clean_guesses(guesses):
    """
    validate input
    """
    #force lower case
    guesses = [(guess[0].lower(),guess[1].lower()) for guess in guesses]

    for guess in guesses:
       # ensure valid colors entered
       valid_responses = ['b','y','g']
       diff = [item for item in guess[1] if item not in valid_responses]
       assert len(diff) == 0, "invalid color" 
       # ensure correct leng
       assert (len(guess[0]) == 5 and len (guess[1]) == 5), "invalid length"
    return guesses


def prod_lst(list):
    """
    calculate product of list with base python
    """
    prod=1
    for x in list:
        prod *= x
    return prod


def word_scores(tokens, corpus, does_contain_list):
    """
    Return the the optimum guess from a corpus
    """
    word_scores =[]
    for word in corpus:
        word_lst = list(set(word))
        # strip out does contain letters
        word_lst = [letter for letter in word_lst if letter not in does_contain_list]
        # score each word as product of token count
        word_score = prod_lst([dict(tokens)[letter] for letter in word_lst])
        word_scores.append([word, word_score])
    # order list
    word_scores.sort(key=lambda x: x[1], reverse= True) 
    return word_scores


def main(guesses):
    """
    Orchastrate result and ouput results
    """
    guesses = clean_guesses(guesses)
    does_contain_list =contains(guesses, does_contain=True)
    # test for too many letters
    assert len(does_contain_list)<= 5, "more then 5 matching letters"

    re_not_like = get_re_not_like(guesses)
    re_like= get_re_like(guesses)

    does_not_contain_list= contains (guesses, does_contain=False)
    # test for conflicting input
    assert not any( letter in does_not_contain_list 
                for letter in does_contain_list), "letter conflict"

    corpus = get_corpus()
    matching = search_corpus(does_not_contain_list, does_contain_list
                , re_not_like, re_like, corpus)
    tokens = count_tokens(matching,1)
    # remove known letters
    tokens = [(x[0], x[1]) for x in tokens if x[0] not in does_contain_list] 

    # Determine next guess
    next_guess = word_scores(tokens, matching, does_contain_list)
    #next_guess_lst = [x[0] for x in next_guess]
    print('-'*50)
    print(f'Guesses        \t {", ".join([x[0] for x in guesses][:10])}')
    print(f'Next guess:    \t {next_guess[0][0]}')
    print(f'Possibilities: \t {len(matching)} out of {len(corpus)}')
    print(f'Top matches:   \t {", ".join([x[0] for x in next_guess][:10])}')
    print('-'*50)
    print('')

guesses = [  ('react', 'byybb')
            ,('glean', 'byyyb')
            #,('salve', 'ygybg')
            ]
main(guesses)