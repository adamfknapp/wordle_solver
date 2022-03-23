import wordle_solver


def print_res(output, guesses):
    print('-'*50)
    print(f'Guesses        \t {", ".join(x[0] for x in guesses)}')
    print(f'Next guess:    \t { output["next_guess"] }')
    print(f'Possibilities: \t {output["possible"]} out of {output["total_words"]}')
    top_match_lst = [x[0] for x in output["top_matches"]]
    print(f'Top matches:   \t {", ".join(top_match_lst)}')
    print('-'*50)
    print('')


def print_ideal_path(ideal_path):
    print('-'*50)
    print(f'Start word:   \t {ideal_path[0][0]}')
    print(f'Total guess:  \t {len(ideal_path)}')
    print(f'Path:         \t {" > ".join(x[0] for x in ideal_path)}')
    print('-'*50)
    print('')


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


def get_ideal_path(first_guess, answer):
    guesses= []
    max_guesses = 6
    for guess in range(max_guesses):
        if guess == 0:
            guess_feedback = get_guess_feedback(first_guess, answer)
            guesses.append((first_guess, guess_feedback))
            if guess_feedback == 'ggggg':
                break
        else:
            next_guess_data = wordle_solver.main(guesses) 
            next_guess = next_guess_data["next_guess"]
            guess_feedback = get_guess_feedback(next_guess, answer)
            guesses.append((next_guess, guess_feedback))
            if guess_feedback == 'ggggg':
                break   
    return guesses

first_guess = 'trash'
answer = 'slosh'
ideal_path = get_ideal_path(first_guess, answer)
print_ideal_path(ideal_path)



#guesses = [
          #('trash', 'bbbgg')
          #,('flush','bgbgg')
          #,('slimy', 'ggbbb')
        #]
#results = get_guess_feedback(guess, answer)
#print(results)
#x = wordle_solver.main(guesses)
#print_res(x, guesses)


