#!/usr/bin/env python3

from collections import Counter
from functools import reduce
from operator import itemgetter
from statistics import mean

import nltk
from nltk import edit_distance
from nltk import jaccard_distance
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams


def setup():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('words')


def _ngrams(word: str, ngram_length):
    return set(ngrams(word, ngram_length))


def jaccard(word, ngram_length):
    """
    The Jaccard index, also known as Intersection over Union and the Jaccard similarity coefficient
    """
    first_char = word[0].lower()
    ngrams_word = _ngrams(word, ngram_length)

    return min(
        (w for w in correct_spellings if w[0].lower() == first_char),
        key=lambda w: jaccard_distance(_ngrams(w, ngram_length), ngrams_word)
    )


def edit_dist_best_match(word):
    """
    Edit Distance (a.k.a. Levenshtein Distance) is a measure of similarity between two strings
    """
    first_char = word[0].lower()

    return min(
        (w for w in correct_spellings if w[0].lower() == first_char),
        key=lambda w: edit_distance(w, word)
    )


def example_three():
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(w, 'v') for w in text1]

    return len(set(lemmatized))


def answer_one():
    return len(set(moby_tokens)) / len(moby_tokens)


def answer_two():
    return sum(1 for token in moby_tokens if token.lower() == "whale") / len(moby_tokens)


def answer_three():
    return Counter(moby_tokens).most_common(20)


def answer_four():
    tokens = [
        token
        for token, token_freq in Counter(moby_tokens).items()
        if (len(token) > 5) and (token_freq > 150)
    ]
    return sorted(tokens)


def answer_five():
    longest_word = reduce(
        lambda a, b: a if len(a) > len(b) else b,
        moby_tokens
    )
    return longest_word, len(longest_word)


def answer_six():
    most_common_words = [
        (freq, token)
        for token, freq in Counter(moby_tokens).items()
        if token.isalpha() and (freq > 2000)
    ]
    return sorted(most_common_words, key=itemgetter(0), reverse=True)


def answer_seven():
    return mean(
        len(nltk.word_tokenize(sentense))
        for sentense in nltk.sent_tokenize(moby_raw)
    )


def answer_eight():
    tags = nltk.pos_tag(moby_tokens)
    return Counter(pos for token, pos in tags).most_common(5)


def answer_nine(entries=('cormulent', 'incendenece', 'validrate')):
    return [jaccard(entry, 3) for entry in entries]


def answer_ten(entries=('cormulent', 'incendenece', 'validrate')):
    return [jaccard(entry, 4) for entry in entries]


def answer_eleven(entries=('cormulent', 'incendenece', 'validrate')):
    return [edit_dist_best_match(entry) for entry in entries]


if __name__ == '__main__':
    # If you would like to work with the raw text you can use 'moby_raw'
    with open('moby.txt', 'r') as f:
        moby_raw = f.read()

    # If you would like to work with the novel in nltk.Text format you can use 'text1'
    moby_tokens = nltk.word_tokenize(moby_raw)
    text1 = nltk.Text(moby_tokens)
    correct_spellings = words.words()
