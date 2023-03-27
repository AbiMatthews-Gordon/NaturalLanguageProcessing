import nltk
from nltk.tokenize import word_tokenize


class PosTagger:

    def tag_pos(tokens):
        pos_tokens = nltk.pos_tag(tokens)
        return pos_tokens

