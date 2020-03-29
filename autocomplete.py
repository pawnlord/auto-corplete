import os
from _thread import *
import threading
import time
import threadclass
import msvcrt


dictionary = []
dictionary.append("")
word = ""
length_weight = 0.5

def nonstoppinginput(word, prompt=""):
    print(prompt + word, end='')
    current = word
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13 or chr == '\n':
                current = ""
                break
            elif ord(chr) >= 32:
                current+= chr.decode('utf-8')
                break
    print ('')  # needed to move to next line
    return current
    

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
guessed_word = ""
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
    if guess != guessed_word:
        print("GUESSED WORD: ", guess)
    guessed_word = guess
    time.sleep(1)
word[0] = ""
autot = threadclass.basicthread(autocomplete)
while True:
    autot = threadclass.basicthread(autocomplete, True)
    if autot.running[0] == False:
        autot.begin(False, name="AUTOCOMPLETE")
    word[0] = nonstoppinginput(word[0], "YOUR WORD: ")
    if word[0] == "EXITNOW":
        break
autot.running[0] = False
