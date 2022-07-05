import tokenize
import re

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import ngrams


class Tokenizer:

    def tokenize(text):
        tokens = word_tokenize(text)
        return tokens

    @staticmethod
    def sentence_tokenizer(text):
        sentences = sent_tokenize(text, language='english')
        return sentences

    @staticmethod
    def n_gram_tokenize(n, tokens):
        n_gram_tokens = list(ngrams(tokens, n))
        return n_gram_tokens

    def remove_stop_words(tokens):
        # nltk.download('stopwords')
        stop_words = nltk.corpus.stopwords.words('english')
        # TODO:: extend stopwords list

        token_stop_words = [sw for sw in tokens
                            if sw and sw in stop_words]
        return token_stop_words

    def normalized_tokens(tokens):
        # remove punctuations etc
        normalized_tokens = [token for token in tokens if token.isalpha()]
        # lowercase tokens
        normalized_tokens = [token.lower() for token in normalized_tokens]
        return normalized_tokens


