import os
from _thread import *
import threading
import time
import msvcrt

dictionary = []
dictionary.append("")
word = ""
length_weight = 0.5


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

def autocomplete(word, possibilities): 
    curr_word = ""
    for c in word:
        if c == ' ':
            possibililities.append(word)
            curr_word = ""
        else:
            curr_word += c
    #print("possibilities" + str(possibilities))
    print("Word: " + curr_word)    
    guess = ""
    current_best = 0
    print(str(possibilities))
    for i in range(len(possibilities)):
        score = score_similarity(curr_word, possibilities[i])
        if score > current_best:
            print(score)
            guess = ""
            guess = possibilities[i]
            current_best = score
    return guess
while True:
    word = input()
    print(autocomplete(word, dictionary))
    
