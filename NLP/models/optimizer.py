import nltk
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words, wordnet
import truecase
from nltk import RegexpParser
from nltk.tokenize.treebank import TreebankWordDetokenizer
# from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from NLP.models.dictionary import Dictionary

class Optimizer:
    @staticmethod
    def optimise(text):
        return Optimizer.remove_duplicate_words(text)
        # return Optimizer.spell_check(text)

    @staticmethod
    def spell_check(text):
        # nltk.download("words")
        correct_words = words.words()

        for word in text:
            if word not in correct_words:
                # and word not in correct_words:
                temp = [(jaccard_distance(set(ngrams(word, 2)),
                                          set(ngrams(w, 2))
                                          ), w)
                         for w in correct_words if w[0]==word[0]]
                corrected_words = sorted(temp, key = lambda val:val[0])[0][1]
                print(corrected_words)
        return corrected_words

    #     #eg. The vehicle is around the corna-> The vehicle is around the corner.
    def change_informal_words(tokens):
        informal_words = Dictionary.informal_words
        for index, token in enumerate(tokens):
            if informal_words.get(token):
               tokens[index] = informal_words.get(token)
        return tokens

    # remove duplicate words unless they are on the allowed duplicates list
    @staticmethod
    def remove_duplicate_words(tokens):  # eg. "He he went to to the gym." -> He went to the gym.
        # print('\033[94m #1 REMOVING REPEATING WORDS...\033[0m \n ')
        num_of_tokens = len(tokens)
        allowed_list = ["the"]
        sanitizedWords = [token for index, token in enumerate(tokens)
                          if ((index + 1) < num_of_tokens) and
                          tokens[index + 1] and
                          (
                                  tokens[index + 1].lower() != token.lower() or
                                  (tokens[index + 2].lower() != token.lower() and token.lower() in allowed_list)
                          ) or
                          ((index + 1) == num_of_tokens) # catches last token
                          ]

        # print(sanitizedWords)
        # TODO: Reconstruct sentence
        # sentence = TreebankWordDetokenizer().detokenize(noduplist)
        # tree = Optimizer.regenerate_parse_tree(sentence)
        return sanitizedWords  # returns the new list

    def remove_duplicate_sentences(sentences): # eg. "The boy ran. The boy ran." should result in "The boy ran."
        num_of_sentences = len(sentences)
        allowed_list = []
        sanitizedSentences = [Optimizer.capitalize_proper_nouns(sentence.capitalize()) for index, sentence in enumerate(sentences)
                          if ((index + 1) < num_of_sentences) and
                          sentences[index + 1] and
                          (
                                  sentences[index + 1].lower() != sentence.lower() or
                                  (sentences[index + 2].lower() != sentence.lower() and sentence.lower() in allowed_list)
                          ) or
                          ((index + 1) == num_of_sentences) # catches last token
                          ]

        return sanitizedSentences

    def capitalize_proper_nouns(text):
        true_cased_text = truecase.get_truecaser().get_true_case(text)

        return true_cased_text

    def remove_grammar_redundancies(tokens):
        stemmer = PorterStemmer()
        num_of_tokens = len(tokens)
        sanitized_tokens = []
        print(tokens)
        for index, token in enumerate(tokens):
            synonyms = [lemma for syn in wordnet.synsets(token) for lemma in syn.lemma_names()]  # we use nltk's wordnet synonym library
            stemmatised_neighbour = ' '.join( [stemmer.stem(w).strip("'") for w in tokens[index - 1].split()] )
            print(stemmatised_neighbour + " " + token)
            if (index < num_of_tokens and tokens[index - 1] and stemmatised_neighbour in synonyms):
                # do not keep word if previous word is a synonym
                continue
            sanitized_tokens.append(token) # keep token if no synonym found

        return sanitized_tokens


    @staticmethod
    def remove_redundant_apostrophes(tokens):
        # eg. The girls's soccer game was delayed by rain. ->
        # The girls' soccer game was delayed by rain.
        # sanitised_tokens = []

        for index, token in enumerate(tokens):
            if token == "'s" and tokens[(index-1)].endswith("s"):
                tokens[index] = "'"
        return tokens

    @staticmethod
    def split_independent_clauses(pos_sentences):
        # eg. I went to the store I got milk and cookies  ->
        # I went to the store. I got milk and cookies.
        pos_sentences_updated = []
        changed = False

        grammar = RegexpParser("""
                                   IC: {<PRP> <V.*> <IN>? <PRP.*>? <NN.*>? <NN.*>? <TO>? <DT>? <NN.*>? <CC>? <NN.*>? <V.*>? <NN.*>}
                                   """)
        for pos_sentence in pos_sentences:
            clauses_updated = False
            independent_clauses = []
            chunk = nltk.tree.Tree.fromstring(str(grammar.parse(pos_sentence)))
            for subtree in chunk.subtrees():
                if subtree.label() == 'IC':
                    if (len(subtree.leaves()) > 4):
                        pos_tokens = Optimizer.convert_leaves_to_tokens(subtree.leaves())
                        sentence = Optimizer.reconstruct_sentence(pos_tokens)
                        sentence = sentence.capitalize()
                        independent_clauses.append(sentence+".")
                        print(sentence)
                        clauses_updated = True
            if (clauses_updated):
                pos_sentences_updated = pos_sentences_updated + independent_clauses
                changed = True
            else:
                pos_sentences_updated.append(Optimizer.reconstruct_sentence(pos_sentence))

        return changed, pos_sentences_updated

    @staticmethod
    def check_subject_verb_agreement(chunk):
        # eg. Anna and Mike is going skiing. -> Anna and Mike are going skiing.
        pos_tokens = Optimizer.convert_leaves_to_tokens(chunk.leaves())
        old_sentence = Optimizer.reconstruct_sentence(pos_tokens)
        sentence_updated = False
        sentence = ''
        changed = False

        for index, leaf in enumerate(chunk.subtrees()):
            if leaf.label() == 'SV1':
                for idx, token in enumerate(pos_tokens):
                    if token[1] == 'VBZ':
                        sentence_updated = True
                        old_token = token
                        new_token = []
                        new_token.append('are')
                        new_token.append('VBD')
                        pos_tokens[idx] = new_token
                        print("\033[91m", old_token, '\033[0m', ' ----------> ', '\033[92m', new_token, '\033[0m')
            if leaf.label() == 'SV2':
                for idx, token in enumerate(pos_tokens):
                    sentence_updated = True
                    if token[1] == 'VBD' or token[0] == 'are':
                        old_token = token
                        new_token = []
                        new_token.append('is')
                        new_token.append('VBZ')
                        pos_tokens[idx] = new_token
                        print("\033[91m", old_token, '\033[0m', ' ----------> ', '\033[92m', new_token, '\033[0m')

        if (sentence_updated):
            updated_sentence = Optimizer.reconstruct_sentence(pos_tokens)
            # print('\033[94m============OLD SENTENCE============\033[0m \n ')
            print(old_sentence)
            # print('\033[94m============UPDATED SENTENCE============\033[0m \n ')
            # print(updated_sentence)
            sentence = updated_sentence
            changed = True
        else:
            # print("No change detected")
            sentence = old_sentence
            changed = False

        return changed, sentence


    @staticmethod
    def convert_leaves_to_tokens(leaves):
        tokens = []
        for leaf in leaves:
            leaf = leaf.split("/")
            tokens.append(leaf)
        return tokens


    @staticmethod
    def reconstruct_sentence(pos_tokens):
        tokens = []
        for token in pos_tokens:
            tokens.append(token[0])

        sentence = TreebankWordDetokenizer().detokenize(tokens)
        return sentence