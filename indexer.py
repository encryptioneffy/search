from array import array
import sys
import file_io
import xml.etree.ElementTree as et
import nltk
import re
import math
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer

class Indexer:
    def __init__(self, xml_file, title_file, doc_file, word_file):
        self.xml_file = sys.argv[1]
        self.title_file = sys.argv[2]
        self.doc_file = sys.argv[3]
        self.word_file = sys.argv[4]
        self.title_dict = {}
        self.doc_dict = {}
        self.word_dict = {}
        root = et.parse(sys.argv[1]).getroot()
        self.all_pages = root.findall("page")
        self.words_to_id_to_count = {}
        self.page_to_links = {}

    def tokenize_stop_stem(page_text : str) -> list:
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        l_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        nltk_stemmer = PorterStemmer()
        tokenized_words = []
        list_of_link_titles = [] #set of all page titles this page_text links to

        # TOKENIZE
        page_tokens = re.findall(n_regex, page_text)

        for word in page_tokens:
            # identifying links in text, storing them for when we do PageRank 
            if re.match('''\[\[[^\[]+?\]\]''', word) != None:
                if "|" in word:
                    link_title, link_text = word.split("|")
                    link_text_tokens = re.findall(n_regex, link_text) 

                    # we can play around with how we wanna store links. 
                    # Do we want to put it in dict immediately? Or just have
                    # the helper function output the inner set that will be 
                    # the value of the linking dict?
                    # currenty I am just storing it as a set of link titles
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

    def make_title_dict(self):
        for page in self.all_pages:
            id: int = page.find("id").text
            title: str = page.find('title').text
            self.title_dict[id] = title
        write_title_file(self.title_file, self.title_dict)

    def make_word_dict(self):
        for page in self.all_pages:
            text: str = page.find("text").text
            id: int = page.find("id").text
            # all_words = re.findall(n_regex, text)
            # all_words is a list of tokenize/stemmed/stopped words for a given page
            all_words_in_page = self.tokenize_stop_stem(text)[0]
            self.page_to_links[id] = self.tokenize_stop_stem(text)[1]


            words_to_id_tf = {}
            max_count = 0

            for word in all_words_in_page: 

                if word in self.words_to_id_to_count:
                    # might cause problem w diff ids idk tho
                    self.words_to_id_to_count[word][id] += 1
                    if self.words_to_id_to_count[word][id] > max_count:
                        max_count = self.words_to_id_to_count[word][id]
                else:
                    self.words_to_id_to_count[word][id] = 1
                    
            for word in all_words_in_page:
                words_to_id_tf[word][id] = (self.words_to_id_to_count[word][id]) / max_count

        n = len(self.all_pages)
        words_to_idf = {}

        for word in self.words_to_id_to_count:
            n_i = len(self.words_to_id_to_count[word])
            words_to_idf[word] = math.log(n/n_i)
        for page in self.all_pages:
            id: int = page.find("id").text
            self.word_file[word][id] = words_to_id_tf[word][id] * words_to_idf[word]
        
        file_io.write_words_file(sys.argv[4], self.word_file)

        






# words_to_id_to_count ={}
# def write_words_file(dict: words_file):
#     n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
#     for page in all_pages:
#         text: str = page.find("text").text
#         id: int = page.find("id").text
#         all_words = re.findall(n_regex, text)
#         # all_words = text.split(" ") #getting list of allwords
#         #NEED TO STEM AND REMOVE STOP WORDS
#         words_to_tf = {}
#         words_to_idf ={}
#         for word in all_words: 
#             words_to_id_to_count[word][id] = all_words.count(word)

# # # sys.argv = 1, 2, 3

# print(sys.argv)
