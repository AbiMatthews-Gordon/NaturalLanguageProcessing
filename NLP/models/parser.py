import nltk
from nltk import RegexpParser
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

import os
import IPython
import svgling
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

# from models.lexical_analyzer import LexicalAnalyser


class Parser:

    def generate_parser_tree(pos_tokens_sentences, tree_folder_name):

        grammar = RegexpParser("""
                               PS: {<PRP> <VBP> <DT>? <IN>? <PR.*> <NN.*>}
                               VP: {<RB>? <CC>? <V.*> <P.*> <IN> <DT> <NN.*>}           #To extract Verb Phrases
                               SV1: {<NN.*> <CC> <NN.*>}
                               SV2: {<NN.*> <CC>}
                               NP: {<DT>?<JJ.*>*<NN.*>+}
                               P: {<IN>}
                               PP: {<IN> <NP>} #To extract Prepositional Phrases
                               # VP: {<V> <NP|PP>*}
                               FW: {<FW>}
                               CD: {<CD>}
                               PRP: {<PRP.*>}
                            """)
        extractions = []
        parse_tree_image_links = []
        for index, sentence in enumerate(pos_tokens_sentences):
            output = grammar.parse(sentence)
            extractions.append(output)
            print("\033[94m Extraction result for sentence \033[0m \n", output)

            Parser.draw_tree(output, "static\\" + tree_folder_name + "\\_" + str(index))
            parse_tree_image_links.append("static/" + tree_folder_name + "/_" + str(index)+".svg")

        return {"parse_tree": extractions, "parser_tree_image_links": parse_tree_image_links}
            # canvasFrame = CanvasFrame()
            # treeWidget = TreeWidget(canvasFrame.canvas(), output)
            # canvasFrame.add_widget(treeWidget,10,10)
            # canvasFrame.print_to_file('tree.ps')
            # output.draw()


    def print_named_entities(pos_sentences):

        named_entities =[]
        # nltk.download('maxent_ne_chunker')
        # nltk.download('words')
        for sentence in pos_sentences:
            ne_tree = nltk.ne_chunk(sentence)
            print("\n\033[94m*******Named Entity Tree*******\033[0m \n", ne_tree)

            # for tree in ne_tree:
            #     if hasattr(tree, 'label'):
            #         named_entities.append(tree.label() + ' _ ' + ' '.join(attribute[0] for attribute in tree))
            # print("\n\033[94m*******Named Entity Trees*******\033[0m \n", named_entities)
        return ne_tree


    @staticmethod
    def draw_tree(tree, name):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        svgname = name+".svg"
        # pdfname = name+".pdf"
        img = svgling.draw_tree(tree)
        svg_data = img.get_svg()
        svg_data.saveas(filename=svgname)

        # drawing = svg2rlg((dirpath+"\\..\\"+svgname))
        # print((dirpath+"..\\"+svgname))
        # renderPDF.drawToFile(drawing, pdfname, autoSize=1)

