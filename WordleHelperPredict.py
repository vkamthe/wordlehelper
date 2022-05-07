# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import csv
import pandas as pd
word_stat_dict = pd.read_csv('dict_new.csv')

# +
#word_stat_dict

# +
# Print to find the first few entries in dictionary!
#list(word_stat_dict.items())[:10]
# -

WORD_LENGTH = 5
ALLOWED_ATTEMPTS = 6

import streamlit as st
import random


def input_word(attempt):
    key1='word'+str(attempt)
    while True:
        word = st.text_input("Input the word you entered> ", key=key1)
        if len(word) == WORD_LENGTH and word.lower() in list(word_stat_dict.word):
            break
    return word.lower()


def input_response(attempt):
    st.write("Type the color-coded reply from Wordle:")
    st.write("  G for Green")
    st.write("  Y for Yellow")
    st.write("  B for Gray")
    
    key2='response'+str(attempt)
    while True:
        response = st.text_input("Response from Wordle> ", key=key2)
        if len(response) == WORD_LENGTH and set(response) <= {"G", "Y", "B"}:
            break
        else:
            st.write("Error - invalid answer", response)
    return response


import string
set(string.ascii_lowercase)

word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]


# +
#print(word_vector)
# -

def match_word_vector(word, word_vector):
    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True


def match(word_vector, possible_words):
    return possible_words.loc[possible_words.apply(lambda row: match_word_vector(row['word'],word_vector),axis=1)]


def yellow_chars_match(possible_words, yellow_chars):
    chars = set(yellow_chars)
    #return [row for row in possible_words if all((c in row.word) for c in chars)]
    return possible_words.loc[possible_words.apply(lambda row: all((c in row['word']) for c in chars),axis=1)]


def solve():
    st.write("This program will help you find the next best word to enter in Wordle")
    st.write("You will get list of words, sorted with probability, to enter, maximum benefit arising from word on top")
    st.write("Along with words, you will also see if word is very frequent in english language, more frequent the word, better the chances")
    st.write("You will also see if word is Plural. Plural words will have less chances")    

    possible_words = word_stat_dict.copy()
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    yellow_chars = ''
    for attempt in range(1, ALLOWED_ATTEMPTS + 1):

        st.write("Attempt", attempt, " with", len(possible_words), "possible words")
        #display_word_table(sort_by_word_commonality(possible_words)[:15])
        
        st.write(possible_words[:10])
        
        word = input_word(attempt)
        response = input_response(attempt)
        
        if response == 'GGGGG':
            st.write("Completed Wordle in", attempt , "attempts")
            break

        for idx, letter in enumerate(response):
            if letter == "G":
                word_vector[idx] = {word[idx]}
            elif letter == "Y":
                yellow_chars = yellow_chars + word[idx]
                try:
                    word_vector[idx].remove(word[idx])
                except KeyError:
                    pass
            elif letter == "B":
                for vector in word_vector:
                    try:
                        vector.remove(word[idx])
                    except KeyError:
                        pass
        
        #st.write("word_verctor", word_vector)
        
        possible_words = match(word_vector, possible_words)
        st.write("possible words after word vector match ", len(possible_words))
        #st.write("possible words ", possible_words[0:10])
        
        st.write("yellow characters", yellow_chars)
        possible_words = yellow_chars_match(possible_words, yellow_chars)
        st.write("possible words after yellow chars match ", len(possible_words))
        #st.write("possible words ", possible_words[0:10])
                                          
    if attempt == ALLOWED_ATTEMPTS:
        st.write("Sorry.... I could not help in ", attempt , "attempts")


solve()


