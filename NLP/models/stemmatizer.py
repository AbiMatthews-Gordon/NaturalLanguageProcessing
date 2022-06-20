import re
from nltk.stem.porter import PorterStemmer


class Stemmatizer:

    def stem(tokens):
        stemmer = PorterStemmer()
        stemmed_tokens = []

        for token in tokens:
            stemmed_token = ' '.join( [stemmer.stem(w).strip("'") for w in token.split()] )
            stemmed_tokens.append(stemmed_token)
        return stemmed_tokens
