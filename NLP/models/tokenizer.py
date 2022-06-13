import tokenize
import re

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import ngrams


class Tokenizer:

    def tokenize(text):
        pattern = re.compile(r"([-\s.,;!?])+")
        tokens = pattern.split(text)
        tokens = [x for x in tokens if x and x not in '-\t\n.,;!?']
        return tokens

    @staticmethod
    def sentence_tokenizer(text):
        return sent_tokenize(text)

    @staticmethod
    def n_gram_tokenize(n, tokens):
        n_gram_tokens = list(ngrams(tokens, n))
        return n_gram_tokens

    def remove_stop_words(tokens):
        nltk.download('stopwords')
        stop_words = nltk.corpus.stopwords.words('english')
        # TODO:: extend stopwords list

        token_stop_words = [sw for sw in tokens if sw and sw in stop_words]
        return token_stop_words

    def normalized_tokens(tokens):
        normalized_tokens = [token.lower() for token in tokens]
        return normalized_tokens


