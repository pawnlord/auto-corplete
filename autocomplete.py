import os
from _thread import *
import threading
import time
import threadclass
import platform


dictionary = []
dictionary.append("")
word = ""
length_weight = 0.25 # length doesn't matter as much as actual similar letters, so weight it
need_new_order = False

if platform.platform()[:7] == "Windows": # windows function, uses msvcrt
    import msvcrt
    def nonstoppinginput(word, prompt, next_best):
        global need_new_order
        os.system("cls")
        print(prompt + word, end='\n')
        need_new_order = True
        current = word
        while True:
            if msvcrt.kbhit():
                chr = msvcrt.getche()
                if ord(chr) == 13 or chr == b'\n':
                    current = ""
                    break
                elif chr == b'\x08': # backspace
                    current = current[:len(current)-1]
                    break
                elif ord(chr) == 9 and best[0]!="": # Tab autocomplete
                    last_space = -1
                    for i in range(len(current)):
                        if current[i] == ' ':
                            last_space = i
                    current = current[:last_space+1]
                    current += best[0] # Change last word to whatever is currently stored in the word pointer
                                        # best contains best 3
                    break
                elif chr == b'@' and best[1]!="": # Tab autocomplete
                    last_space = -1
                    for i in range(len(current)):
                        if current[i] == ' ':
                            last_space = i
                    current = current[:last_space+1]
                    current += best[1] # get second best
                    break
                elif chr == b'#' and best[2]!="": # Tab autocomplete
                    last_space = -1
                    for i in range(len(current)):
                        if current[i] == ' ':
                            last_space = i
                    current = current[:last_space+1]
                    current += best[2] # get third best
                    break
                elif ord(chr) >= 32:
                    current+= chr.decode('utf-8')
                    break
        print ('')  # needed to move to next line
        return current
else: # Linux (and Mac if it is supported) should use curses
    print("UNSUPPORTED PLATFORM!")
    exit(1)

with open("words.txt", "r") as ws:
    for c in ws.read():
        if c == '\n' or c == ' ' or c == '\t':
            dictionary.append("") # it's a new word, so make a new word
        else:
            dictionary[len(dictionary)-1] += c # copy word
            

def score_similarity(word1, word2):
    score = 0
    if word1 > word2: # If it's smaller, we can assume they did not want it
        return 0
    score -= abs(len(word1) - len(word2)) * length_weight # subtract from score, proportionaly
    for c in range(min(len(word1), len(word2))):
        if word1[c] == word2[c]: # if there is a similarity, add to the score
            score+=1
        else: # if not, subtract from it proportionally
            # The longer the word, the more likely one is to make a mistake
            # so, mistakes should not be taken as seriously
            score -= 1-(c/min(len(word1), len(word2))) 
    return score
best = ["", "", ""]
guessed_word = [""]
word = [""]
# these are lists so that they can be passed to functions as pointers
# yes it's a hack, but it works

def autocomplete(running): 
    global word, guessed_word, best, dictionary, need_new_order
    
    curr_word = ""
    for c in word[0]:
        if c == ' ':
            dictionary.append(word[0])
            curr_word = "" # if they used a word, they might use it again, so keep it
        else:
            curr_word += c
    guess = ""
    current_best = 0
    for i in range(len(dictionary)):
        score = score_similarity(curr_word.lower(), dictionary[i]) # get similarities
        if score > current_best: # best score wins
            guess = ""
            guess = dictionary[i]
            current_best = score
            best[0], best[1], best[2] = guess, best[0], best[1]
    guessed_word[0] = guess
    if need_new_order:        
        print("GUESSED WORD: " + guessed_word[0] + "\nNEXT BEST: " + str(best[1:]))
        need_new_order = False
word[0] = "" 
try:
    autot = threadclass.basicthread(autocomplete, True) # thread running autocomplete, repeats when stopped
    autot.begin(False, name="AUTOCOMPLETE")
    while True:
        word[0] = nonstoppinginput(word[0], "YOUR WORD: ", best)
        if word[0] == "EXITNOW": # exit condition
            break
    autot.running[0] = False # stops thread
except KeyboardInterrupt:
    print("KeyboardInterrupt CAUGHT")
    autot.running[0] = False # stops thread
    raise 
except Exception as e:
    print("EXCEPTION CAUGHT")
    print(e)
    autot.running[0] = False # stops thread
