import sys
import file_io
import xml.etree.ElementTree as et
import nltk
import re
import math
nltk.download('stopwords')
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

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
        
    
        


    def make_title_dict(self):
        for page in self.all_pages:
            id: int = page.find("id").text
            title: str = page.find('title').text
            self.title_dict[id] = title
        file_io.write_title_file(self.title_file, self.title_dict)

    def make_word_dict(self):
    
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        for page in self.all_pages:
            text: str = page.find("text").text
            id: int = page.find("id").text
            all_words = re.findall(n_regex, text)
        
        #NEED TO STEM AND REMOVE STOP WORDS
            words_to_id_tf = {}
            max_count = 0
            for word in all_words: 

                if word in self.words_to_id_to_count:
                    #might cause problem w diff ids idk tho
                    self.words_to_id_to_count[word][id] += 1
                    if self.words_to_id_to_count[word][id] > max_count:
                        max_count = self.words_to_id_to_count[word][id]
                else:
                    self.words_to_id_to_count[word][id] = 1
            for word in all_words:
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
