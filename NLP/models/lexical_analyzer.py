import nltk
from nltk import tokenize
from NLP.models.tokenizer import Tokenizer
from NLP.models.lemmatizer import Lemmatizer
from NLP.models.pos_tagger import PosTagger
from NLP.models.stemmatizer import Stemmatizer
from NLP.models.parser import Parser
from NLP.models.optimizer import Optimizer
from nltk.tokenize.treebank import TreebankWordDetokenizer


class LexicalAnalyser:

    @staticmethod
    def perform_lexical_analysis(text):

        sentences = Tokenizer.sentence_tokenizer(text)
        # optimised_sentences = Optimizer.remove_duplicate_sentences(sentences)
        sentences = Optimizer.remove_duplicate_sentences(sentences)
        # tokens = Tokenizer.tokenize(text)
        tokens = Tokenizer.tokenize(Optimizer.capitalize_proper_nouns(' '.join(sentences)))
        tokens = Optimizer.change_informal_words(tokens)
        tokens = Optimizer.remove_duplicate_words(tokens)
        tokens = Optimizer.remove_grammar_redundancies(tokens)
        tokens = Optimizer.remove_redundant_apostrophes(tokens)
        sentences = Tokenizer.sentence_tokenizer(TreebankWordDetokenizer().detokenize(tokens))
        two_gram_tokens = Tokenizer.n_gram_tokenize(2, tokens)
        stop_words = Tokenizer.remove_stop_words(tokens)
        normalized_tokens = Tokenizer.normalized_tokens(tokens)
        lemmatized_tokens = Lemmatizer.lemmatize(tokens)
        tokens_pos = PosTagger.tag_pos(tokens)
        stemmed_tokens = Stemmatizer.stem(tokens)

        print('\033[94m*******SENTENCES*******\033[0m \n', sentences)
        print('\033[94m*******TOKENS*******\033[0m \n', tokens)
        # print('\033[94m*******OPTIMISED TOKENS*******\033[0m \n', optimised_tokens)
        # print('\033[94m*******OPTIMISED SENTENCES*******\033[0m \n', optimised_sentences)
        # print('\033[94m*******TWO GRAM TOKENS*******\033[0m \n', two_gram_tokens)
        print('\033[94m*******STOP WORDS*******\033[0m \n', stop_words)
        print('\033[94m*******NORMALIZED TOKENS*******\033[0m \n', normalized_tokens)
        print('\033[94m*******LEMMATIZED TOKENS*******\033[0m \n', lemmatized_tokens)
        print('\033[94m*******PARTS OF SPEECH*******\033[0m \n', tokens_pos)
        print('\033[94m*******STEMMATIZED TOKENS*******\033[0m \n', stemmed_tokens)

        pos_sentences = []

        for sentence in sentences:
            pos_sentence = (PosTagger.tag_pos(Tokenizer.tokenize(sentence)))
            pos_sentences.append(pos_sentence)
        print("-----------------------")
        print(pos_sentences)
        pos_sentences_optimised = Optimizer.split_independent_clauses(pos_sentences)
        print("-----------------------")
        print(pos_sentences_optimised)

        name_entities = Parser.print_named_entities(pos_sentences)
        return pos_sentences
        # return {"sentences": tokens,
        #         "tokens": two_gram_tokens,
        #         "two_gram_tokens": stop_words,
        #         "stop_words": normalized_tokens,
        #         "normalized_tokens": lemmatized_tokens,
        #         "lemmatized_tokens": tokens_pos,
        #         "tokens_pos": stemmed_tokens,
        #         "pos_sentences": pos_sentences
        #         }
