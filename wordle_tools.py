
"""
TODO 
    failed when the answer is 'tease'. Issue with repeat letters?

    support multiple game types
    results: 
"""
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
    #standardize word scores
    top_word_score = word_scores[0][1]
    word_scores = [ (x[0],x[1]/top_word_score) for x in word_scores]
    return word_scores


def get_guess_feedback(guess, answer):
    """
    return string for how guess performed
    """
    res=list('bbbbb')
    for index in range(len(guess)):
        guess_letter = list(guess)[index]
        answer_letter = list(answer)[index]
        if guess_letter == answer_letter:
            res[index] = 'g'
        elif guess_letter in list(answer):
            res[index] = 'y'
        else:
            res[index] = 'b'
    return "".join(res)


def get_next_guess(guesses):
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
    
    dict = {
            'next_guess': next_guess[0][0]
            ,'possible': len(matching)
            ,'total_words': len(corpus)
            , 'top_matches': next_guess[:10]
            }
    return dict


def get_path(first_guess, answer):
    guesses= []
    max_guesses = 6
    for guess in range(max_guesses):
        if guess == 0:
            guess_feedback = get_guess_feedback(first_guess, answer)
            guesses.append((first_guess, guess_feedback))
            if guess_feedback == 'ggggg':
                break
        else:
            next_guess_data = get_next_guess(guesses) 
            next_guess = next_guess_data["next_guess"]
            guess_feedback = get_guess_feedback(next_guess, answer)
            guesses.append((next_guess, guess_feedback))
            if guess_feedback == 'ggggg':
                break   
    return guesses
