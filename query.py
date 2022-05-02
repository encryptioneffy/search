from array import array
import sys
import file_io
from file_io import *
import xml.etree.ElementTree as et
import nltk
import re
import math
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer

# the read_titles function does not return anything; 
# it populates the blank dictionary it takes in

class Query:
    def __init__(self):
        if len(sys.argv) == 5:
            self.page_rank_yn = True
            self.title_file = sys.argv[2]
            self.doc_file = sys.arg[3]
            self.word_file = sys.argv[4]
        else:
            self.page_rank_yn = False
            self.title_file = sys.argv[1]
            self.doc_file = sys.argv[2]
            self.word_file = sys.argv[3]

        self.title_dict = {}
        read_title_file(self.title_file, self.title_dict)

        self.doc_dict = {}
        read_docs_file(self.doc_file, self.doc_dict)

        self.word_dict = {}
        read_words_file(self.word_file, self.word_dict)

        self.id_to_scores_dict = {}


    def tokenize_stop_stem(self, page_text : str) -> list:
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        nltk_stemmer = PorterStemmer()
        tokenized_words = []

        page_tokens = re.findall(n_regex, page_text)

        for word in page_tokens:
            word = word.lower()
            if word not in STOP_WORDS:
                tokenized_words.append(nltk_stemmer.stem(word))
        
        return(tokenized_words)

    def make_score_dict(self, query_text : str) -> list:
        query_terms = self.tokenize_stop_stem(query_text)

        for page_id in self.title_dict.keys():
            doc_score = 0

            for word in query_terms:
                score = 0
                if word in self.word_dict.keys():
                    if page_id in self.word_dict[word].keys():
                        score = self.word_dict[word][page_id]
            doc_score += score

            self.id_to_scores_dict[page_id] = doc_score
            # should querier still return a page if no query terms in page?

    
    def make_page_rank_dict(self, query_text : str) -> list:
        query_terms = self.tokenize_stop_stem(query_text)

        for page_id in self.title_dict.keys():
            doc_score = 0

            for word in query_terms:
                score = 0
                if word in self.word_dict.keys():
                    if page_id in self.word_dict[word].keys():
                        score = self.word_dict[word][page_id]
            doc_score += score

            self.id_to_scores_dict[page_id] = doc_score
            
        # should querier still return a page if no query terms in page?

    
    def get_score(self, kv_tuple : tuple) -> float:
        return kv_tuple[1]
    
    def get_title(self, kv_tuple : tuple) -> str:
        return self.title_dict[kv_tuple[0]]
    
    def get_top_ten(self) -> list:
        dict_items = []
        dict_items = self.id_to_scores_dict.items()

        x = sorted(dict_items, key=self.get_score, reverse=True)
        if len(x) > 10:
            top_ten_tuples = x[0:10]
        else:
            top_ten_tuples = x
        
        top_ten_ids = []
        for pair in top_ten_tuples:
            top_ten_ids.append(pair[0])

        top_ten_titles = []
        for id in top_ten_ids:
            top_ten_titles.append(self.title_dict[id])

        return top_ten_titles



if __name__ == "__main__": 
    while True:
        user_input = input(">>search")

        if user_input == ":quit":
            break

        the_querier = Query()
        the_querier.make_score_dict(user_input)
        print(the_querier.get_top_ten())
        