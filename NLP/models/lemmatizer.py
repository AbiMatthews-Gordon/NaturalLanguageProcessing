import nltk
from nltk.stem import WordNetLemmatizer


class Lemmatizer:

    def lemmatize(tokens):

        # nltk.download('wordnet')
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = []

        for token in tokens:
            lemmatized_tokens.append(lemmatizer.lemmatize(token))
        return lemmatized_tokens
