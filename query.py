from array import array
from ast import Index
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
import os.path
from os.path import exists

# the read_titles function does not return anything; 
# it populates the blank dictionary it takes in
'''
Query class
'''
class Query:
    def __init__(self):
        if len(sys.argv) == 5:
            if os.path.exists(sys.argv[2]) and os.path.exists(sys.argv[3]) and os.path.exists(sys.argv[4]):
                self.page_rank_yn = True
                self.title_file = sys.argv[2]
                self.doc_file = sys.argv[3]
                self.word_file = sys.argv[4]
            else:
                raise ValueError("invalid file paths")
        elif len(sys.argv) == 4:
            if os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]) and os.path.exists(sys.argv[3]):
                self.page_rank_yn = False
                self.title_file = sys.argv[1]
                self.doc_file = sys.argv[2]
                self.word_file = sys.argv[3]
            else: 
                raise ValueError("invalid file paths")
        else:
            raise IndexError("invalid number of inputs")

        self.title_dict = {}
        read_title_file(self.title_file, self.title_dict)

        self.doc_dict = {}
        read_docs_file(self.doc_file, self.doc_dict)

        self.word_dict = {}
        read_words_file(self.word_file, self.word_dict)

        self.id_to_scores_dict = {}

    '''
    Tokenizes, removes stop words, and stems words
    Parameters:
        page_text -- string of the text in a page
    
        Returns:
        list of the tokenized, stopped, and stemmed words

        Raise:
        ValueError if all words int he search are stop words
    '''
    def tokenize_stop_stem(self, page_text : str) -> list:
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        nltk_stemmer = PorterStemmer()
        tokenized_words = []

        page_tokens = re.findall(n_regex, page_text)

        for word in page_tokens:
            word = word.lower()
            if word not in STOP_WORDS:
                tokenized_words.append(nltk_stemmer.stem(word))
        if len(tokenized_words) == 0:
            raise ValueError("all query words are stop words")
        else:
            return(tokenized_words)
    '''
    calculates the score for each page and puts score in dictionary for each page id
    Parameters:
        query_text -- string of the text from query
    '''
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

    '''
    Creates a pagerank dctionary if given pagerank in query
    Parameters:
        page_text -- string of the text in a page
    '''
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

            self.id_to_scores_dict[page_id] = doc_score * self.doc_dict[page_id]
            
        # should querier still return a page if no query terms in page?

    '''
    Returns the score of the page????????
    Parameters:
        page_text -- string of the text in a page
    
        Returns:
        list of the tokenized, stopped, and stemmed words
    '''
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
            if pair[1] > 0:
                top_ten_ids.append(pair[0])

        top_ten_titles = []
        for id in top_ten_ids:
            top_ten_titles.append(self.title_dict[id])

        return top_ten_titles


'''
Main method for Query

    Raise:
    IndexError if invalid number of inputs for sys.argv
'''
if __name__ == "__main__": 
        try:
            if len(sys.argv) < 4 or len(sys.argv) > 5:
                raise IndexError("invalid number of inputs")
            while True:
                the_querier = Query()
                user_input = input(">>search")
                if user_input == ":quit":
                    break
                if the_querier.page_rank_yn:
                    the_querier.make_page_rank_dict(user_input)
                else:
                    the_querier.make_score_dict(user_input)
                
                print(the_querier.get_top_ten())
        except IndexError as e:
            print("invalid number of inputs")
        except ValueError as e:
            print(e)
        except Exception as e:
            if user_input == "" or user_input == " ":
                print("please do not leave the search query blank")


        