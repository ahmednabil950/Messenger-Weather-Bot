from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import treebank_chunk
from nltk import Tree
from nltk.chunk import tree2conlltags

# sentence = "What is the weather in"

# sentence = "How is the weather like in Chicago"


# ne_tagged = ne_chunk(pos_tag(word_tokenize(sentence)))

# print(tree2conlltags(ne_tagged))

######################################################################################################
######################################################################################################

def get_chunks(text, label):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    current_chunk = []

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == label:
            current_chunk.append(
                " ".join([token for token, pos in subtree.leaves()]))

    return current_chunk


######################################################################################################
######################################################################################################


# print(get_chunks(sentence, 'GPE'))

######################################################################################################
######################################################################################################
