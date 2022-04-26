from array import array
import sys
import file_io
import xml.etree.ElementTree as et
import re
import math
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
# nltk_test = PorterStemmer()
# nltk_test.stem("Stemming")

'''text1 = "Hey! My name is EFfy and I like [[Sharks|Hammerheads]]. I do NOT like [[Whale]] [[Sharks]]. By the way, Mom asked [[How are you?]]. She is worried worry about the [[Presidents|Losing Money]]. Now we are stemming some cheesy, running, and funny English word words. Going to sleep sleeps slept sleeping."
'''

'''This function successfully tokenizes a really long string into a list 
of lower case words-strings, with Link Titles removed, multi-word Link Text  
included in the corpus, and all words stopped & stemmed. '''

'''We should play around with how tokenize, stop, stem are organized. Will they 
be in separate helper functions? Or altogether in 1 function? Which version
will minimize the amount of times we have to loop through a list? '''

def tokenize_stop_stem(page_text : str) -> list:
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        l_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        nltk_stemmer = PorterStemmer()
        tokenized_words = []
        list_of_link_titles = [] #list of all the page titles this page_text links to

        # TOKENIZE
        page_tokens = re.findall(n_regex, page_text)

        for word in page_tokens:
            # identifying links in text, storing them for when we do PageRank later
            if re.match('''\[\[[^\[]+?\]\]''', word) != None:
                if "|" in word:
                    pipe_link_stuff = word.split("|")
                    link_title = pipe_link_stuff[0]
                    link_text = pipe_link_stuff[1]
                    link_text_tokens = re.findall(n_regex, link_text) 

                    link_title = link_title.replace("[[", "")
                else: 
                    link_text_tokens = re.findall(l_regex, word)
                    link_title = word.strip("[[]]")
                
                # STOP
                link_words = filter(lambda x: x not in STOP_WORDS, \
                    map(str.lower, link_text_tokens))
                # STEM
                link_words = map(lambda x: nltk_stemmer.stem(x), link_words)
                tokenized_words += link_words

                # saves link_title to a data structure, making sure
                # there are no duplicate links stored for given page_text
                if link_title not in list_of_link_titles:
                    list_of_link_titles.append(link_title)
            else:
                word = word.lower()
                if word not in STOP_WORDS:
                    tokenized_words.append(nltk_stemmer.stem(word))
        
        return(tokenized_words, list_of_link_titles)

# (1) add link_text to the corpus, but make sure to treat
# like any other text: parse, tokenize, stop, and stem it. 
# ESPECIALLY is it is multi-word link_text like "how are you"!
# From EdStem:
# '[[how are you]]' is an example of a link without a pipe, 
# for which you would count 'how are you' as a title and 
# process each word. This means you should treat "how are you" 
# like any other text: tokenize, remove stop words, stem, etc.
# (2) add link_title to wherever you are storing page links