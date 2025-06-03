from os import system as sys
from time import sleep
import re

#VARIABLES
form_filename = 'spellingbee_sample.txt'
data_filename = 'spellingbee_data.txt'
main_letter = ""
letters = ""
words = []
found_words = []
sample = []

#FOR COMMENTS
nice_guy = "(≧◡≦)  " 
bad_guy =  "(￢_￢;)  "
codes_dict_nice = {-1: "Sweetie, you've found a word! Your parents must be proud of you!",
0: "Your input is empty.",
1: "Sweetie, it'd be better if you used only Latin letters.",
2: "Watch the honeycombs: they show which letters you can use!",
3: "Sweetie, do not forget where all roads lead!",
4: "It's too short, unfortunately...",
5: "I wish it was real...",
6: "It's a nice try, but I think you've already found it."}
codes_dict_bad = {-1: "You've finally found it. Congratulations.",
              0: "It's empty! Or it means you give up?))",
              1: "Words aren't just random gibberish - they're built from letters!",
              2: "These pretty honeycombs aren't decoration. There are letters on them!",
              3: "Remind me: where do all roads lead?",
              4: "I believe you can come up with something longer.", 
              5: "Think again.",
              6: "You've already found it."}

#READ FILES (SAMPLE AND DATA)
with open(form_filename) as afile:
    data = afile.readlines()
    with open (data_filename) as afile2:
        main_letter = afile2.readline().strip()
        letters = (main_letter + afile2.readline()).replace('\n','')
        words = list(map(lambda s: (s.strip()).upper(), afile2.readlines()))

    replace_base = data[0].strip()
    greeting = data[1] + data[2] + data[3].replace('?',main_letter)
    sample = "*".join(data[4:])
    for i in range(len(replace_base)):
        sample = sample.replace(replace_base[i], letters[i])
    sample = [greeting] + sample.split("*")


def make_output_sample(sample, found_words):
    new_sample = sample.copy()
    if found_words:
        last_str = 3
        maxlen = len(max(found_words, key=len))
        for i, word in enumerate(found_words):
            if i!=0 and i%4==0: 
                new_sample[last_str] += '\n' 
                last_str += 1
            another_word = f'{i+1}){word}'
            new_sample[last_str] = new_sample[last_str][:-2] + f'{another_word:<{maxlen+4}}' + "  "

        new_sample[last_str] += '\n'

    return new_sample


def check_input(user_input, found_words, words, letters, main_letter):
    code = -1
    user_input = user_input.upper()

    if not user_input:
        code = 0
    elif not bool(re.fullmatch(r'[A-Z]+', user_input)):
        code = 1
    elif not set(user_input).issubset(set(letters)):
        code = 2
    elif main_letter not in user_input:
        code = 3
    elif len(user_input) <= 3:
        code = 4
    elif user_input not in words:
        code = 5
    elif user_input in found_words:
        code = 6
    
    return code


def dramatic_print(dramatic_message, dramatic_delay, dramatic_pause):
    for dramatic_c in dramatic_message:
        print(dramatic_c, end='',flush=True)
        sleep(dramatic_delay)
    sleep(dramatic_pause)


def dramatic_end():
    sys("cls")
    sleep(3)
    dramatic_print("You know", 0.1, 2)
    dramatic_print("...", 0.3, 2)
    sys("cls")
    dramatic_print("I tried to be patient. ", 0.1, 2)
    sys("cls")
    dramatic_print("I gave you a chance", 0.1, 1)
    dramatic_print("... ", 0.3, 3)
    sys("cls")
    dramatic_print("But you lost it.", 0.25, 3)
    sys("cls")
    sleep(1)
    dramatic_print("Goodbye.", 0, 1.5)
    sys("cls")


def help_option():
    global bad_guy
    sys("cls")
    print(bad_guy, end='')
    dramatic_print("You want some help?\n", 0.1, 1)
    dramatic_print("You had to say it earlier, sweetie!)\n", 0.1, 1)
    dramatic_print("Here, take this link to the tutorial video - it should help you: ", 0.1, 0.5)
    print("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    sleep(15)
    sys("cls")
    print("(￢‿￢ )")
    dramatic_print("Did it help?)", 0.1, 7)
    

def main():
    user_input = ""
    message = "I hope you know the rules! If not, read them somewhere! \n\t(Or do not - playing without knowing them will make it even more interesting).\n"
    mistakes = 0
    score = 0
    guy = 0
    help_flag = 1

    while user_input.upper() != "XXXXX":
        #SAMPLE
        sys("cls")
        score_message = ""
        output_sample = make_output_sample(sample, found_words)
        print(*output_sample)
        print(message)

        #INPUT
        user_input = input('Input word: ')
        code = check_input(user_input, found_words, words, letters, main_letter)

        #HELP OPTION
        if user_input.lower() == "help" and guy == 1 and help_flag:
            help_option()
            help_flag = 0
            continue

        if code != -1:
            mistakes += 1
        else:
            found_words.append(user_input.upper())
            new_points = 0
            if len(user_input) == 4:
                new_points = 1
            elif len(user_input) in (5,6,7):
                new_points = len(user_input)
            else:
                new_points = len(user_input)*2

            score += new_points
            score_message = f"\n(You earned {new_points} points)."
            mistakes -= min(new_points, mistakes)

        #INPUT RESULT
        if len(found_words) == len(words):
            break

        guy = (mistakes >= 19) + (mistakes >= 13) + (mistakes >= 7)

        if guy == 3: 
            dramatic_end()
            return 1
        elif guy == 2: message = bad_guy + "..." + score_message
        elif guy == 1: message = bad_guy + codes_dict_bad[code] + score_message
        else: message = nice_guy + codes_dict_nice[code] + score_message


    sys("cls")
    guy = (mistakes >= 13) + (mistakes >= 7)
    print(f"(Your total score is {score} points). ")

    if len(found_words) == len(words):
        if guy == 2: print(bad_guy + "You tried.")
        if guy == 1: print(bad_guy + "Well, I've to admit you're better than I thought. Congratulations.")
        if guy == 0: print(nice_guy + "You guessed all the words! That's an impossible result! What a genius! My congratulations!")
    elif len(found_words) >= 1:
        if guy == 2: print(bad_guy + "You tried.")
        if guy == 1: print(bad_guy + f"You guessed {len(found_words)} from {len(words)} words. Not so bad.")
        if guy == 0: print(nice_guy + f"You guessed {len(found_words)} from {len(words)} words! That's an awesome result! My congratulations!")
    else:
        if guy == 2: print(bad_guy + "I didn't even doubt it.")
        if guy == 1: print(bad_guy + "I think we both understand: you got what you deserved.")
        if guy == 0: print(nice_guy + "I know you tried - don't be upset, you'll do it next time! I believe in you!")    
    
        
    sleep(5)
    sys("cls")
    return 0

while True:
    if main(): break 
    if input("Play again (yes/no)?\n").lower() in ('no','nope','n'): 
        break