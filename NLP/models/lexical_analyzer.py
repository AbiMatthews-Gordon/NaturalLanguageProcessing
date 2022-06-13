import nltk
from nltk import tokenize
from models.tokenizer import Tokenizer
from models.lemmatizer import Lemmatizer
from models.pos_tagger import PosTagger
from models.stemmatizer import Stemmatizer


class LexicalAnalyser:

    @staticmethod
    def perform_lexical_analysis(text):

        sentences = Tokenizer.sentence_tokenizer(text)
        tokens = Tokenizer.tokenize(text)
        two_gram_tokens = Tokenizer.n_gram_tokenize(2, tokens)
        stop_words = Tokenizer.remove_stop_words(tokens)
        normalized_tokens = Tokenizer.normalized_tokens(tokens)
        lemmatized_tokens = Lemmatizer.lemmatize(tokens)
        tokens_pos = PosTagger.tag_pos(tokens)
        stemmed_tokens = Stemmatizer.stem(tokens)

        print('\033[94m*******SENTENCES*******\033[0m \n', sentences)
        print('\033[94m*******TOKENS*******\033[0m \n', tokens)
        print('\033[94m*******TWO GRAM TOKENS*******\033[0m \n', two_gram_tokens)
        print('\033[94m*******STOP WORDS*******\033[0m \n', stop_words)
        print('\033[94m*******NORMALIZED TOKENS*******\033[0m \n', normalized_tokens)
        print('\033[94m*******LEMMATIZED TOKENS*******\033[0m \n', lemmatized_tokens)
        print('\033[94m*******PARTS OF SPEECH*******\033[0m \n', tokens_pos)
        print('\033[94m*******STEMMATIZED TOKENS*******\033[0m \n', stemmed_tokens)

        pos_sentences = []

        for sentence in sentences:
            pos_sentence = (PosTagger.tag_pos(Tokenizer.tokenize(sentence)))
            pos_sentences.append(pos_sentence)

        return pos_sentences




