import os
from _thread import *
import threading
import time
import threadclass
import platform


dictionary = []
dictionary.append("")
word = ""
length_weight = 0.5
if platform.platform()[:7] == "Windows":
    import msvcrt
    def nonstoppinginput(word, prompt, wordp):
        os.system("cls")
        print(prompt + word, end='\n')
        current = word
        while True:
            if msvcrt.kbhit():
                chr = msvcrt.getche()
                if ord(chr) == 13 or chr == '\n':
                    current = ""
                    break
                elif ord(chr) == 127:
                    current = current[:-2]
                    break
                elif ord(chr) == 9:
                    last_space = -1
                    for i in range(len(current)):
                        if current[i] == ' ':
                            last_space = i
                    current = current[:last_space+1]
                    current += wordp[0]
                    break
                elif ord(chr) >= 32:
                    current+= chr.decode('utf-8')
                    break
        print ('')  # needed to move to next line
        return current
else:
    print("UNSUPPORTED PLATFORM!")
    exit(1)

with open("words.txt", "r") as ws:
    for c in ws.read():
        if c == '\n' or c == ' ' or c == '\t':
            dictionary.append("")
        else:
            dictionary[len(dictionary)-1] += c
            

def score_similarity(word1, word2):
    score = 0
    if word1 > word2:
        return 0
    score -= abs(len(word1) - len(word2)) * length_weight
    for c in range(min(len(word1), len(word2))):
        if word1[c] == word2[c]:
            score+=1
        else:
            score -= 1-(c/min(len(word1), len(word2)))
    return score
guessed_word = [""]
word = [""]

def autocomplete(running): 
    global word, guessed_word, dictionary
    
    curr_word = ""
    for c in word[0]:
        if c == ' ':
            dictionary.append(word[0])
            curr_word = ""
        else:
            curr_word += c
    #print("possibilities" + str(possibilities))
    guess = ""
    current_best = 0
    for i in range(len(dictionary)):
        score = score_similarity(curr_word, dictionary[i])
        if score > current_best:
            guess = ""
            guess = dictionary[i]
            current_best = score
    if guess != guessed_word[0]:
        print("GUESSED WORD: ", guess)
    guessed_word[0] = guess
    time.sleep(1)
word[0] = ""
try:
    autot = threadclass.basicthread(autocomplete, True)
    autot.begin(False, name="AUTOCOMPLETE")
    while True:
        word[0] = nonstoppinginput(word[0], "YOUR WORD: ", guessed_word)
        if word[0] == "EXITNOW":
            break
    autot.running[0] = False
except KeyboardInterrupt:
    print("KeyboardInterrupt CAUGHT")
    autot.running[0] = False
    raise 
except Exception as e:
    print("EXCEPTION CAUGHT")
    print(e)
    autot.running[0] = False
