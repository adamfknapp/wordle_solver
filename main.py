import wordle_tools


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
    path_str = " -> ".join([f'{x[0]} ({x[1]})' for x in ideal_path])
    print(f'Path:         \t {path_str}')
    print('-'*50)
    print('')


"""
first_guess = 'aideu'
answer = 'fewer'
x = wordle_tools.get_path(first_guess, answer)
print_ideal_path(x)
"""
guesses = [
          ('crane', 'gbbgb')
         ,('clung','gbggb')
         # ,('cobra', 'bgbyy')
         # , ('viper', 'bbbgg')
        ]


x = wordle_tools.get_next_guess(guesses)
print_res(x, guesses)



