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
with open('dict.csv') as csv_file:
    reader = csv.reader(csv_file)
    word_stat_dict = dict(reader)

# +
# Print to find the first few entries in dictionary!
#list(word_stat_dict.items())[:10]
# -

WORD_LENGTH = 5
ALLOWED_ATTEMPTS = 6

import streamlit as st
import random


def input_word(attempt):
    while True:
        key='word'+str(attempt)+str(random.BPF)
        word = st.text_input("Input the word you entered> ", key=key)
        if len(word) == WORD_LENGTH and word.lower() in word_stat_dict:
            break
    return word.lower()


def input_response(attempt):
    st.write("Type the color-coded reply from Wordle:")
    st.write("  G for Green")
    st.write("  Y for Yellow")
    st.write("  ? for Gray")
    
    key='response'+str(attempt)+random.BPF
    while True:
        response = st.text_input("Response from Wordle> ", key=key)
        if len(response) == WORD_LENGTH and set(response) <= {"G", "Y", "?"}:
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


# +
#match_word_vector('99999',word_vector)
# -

def match(word_vector, possible_words):
    return [word for word in possible_words if match_word_vector(word, word_vector)]


def yellow_chars_match(possible_words, yellow_chars):
    chars = set(yellow_chars)
    return [word for word in possible_words if all((c in word) for c in chars)]


def solve():
    possible_words = word_stat_dict.copy()
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    yellow_chars = ''
    for attempt in range(1, ALLOWED_ATTEMPTS + 1):

        st.write("Attempt", attempt, " with", len(possible_words), "possible words")
        #display_word_table(sort_by_word_commonality(possible_words)[:15])
        
        st.write(list(possible_words)[:10])
        
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
            elif letter == "?":
                for vector in word_vector:
                    try:
                        vector.remove(word[idx])
                    except KeyError:
                        pass
        
        possible_words = match(word_vector, possible_words)
        st.write("possible words after word vector match ", len(possible_words))
        
        st.write("yellow characters", yellow_chars)
        possible_words = yellow_chars_match(possible_words, yellow_chars)
        st.write("possible words after yellow chars match ", len(possible_words))
                                            
    if attempt == ALLOWED_ATTEMPTS:
        st.write("Sorry.... I could not help in ", attempt , "attempts")



solve()

random

random.BPF


