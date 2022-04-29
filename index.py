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

class Indexer:
    def __init__(self, xml_file, title_file, doc_file, word_file):
        self.xml_file = sys.argv[1]
        self.title_file = sys.argv[2]
        self.doc_file = sys.argv[3]
        self.word_file = sys.argv[4]
        self.id_to_title_dict = {}
        self.title_to_id_dict = {}
        self.doc_dict = {}
        self.word_dict = {}
        root = et.parse(sys.argv[1]).getroot()
        self.all_pages = root.findall("page")
        self.words_to_id_to_count = {}
        self.page_to_links = {}
        self.graph_dict = {}
        self.id_to_linked_ids = {}
        self.n = len(self.all_pages)
        self.weight_dict = {}
        self.old_rank_dict = {}
        self.new_rank_dict = {}

        self.make_title_dict()
        self.make_word_dict()
        self.make_id_to_link_dict()
        self.weight_calculator()
        self.make_doc_dict()
        
        

    def tokenize_stop_stem(self, page_text : str) -> list:
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        l_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        nltk_stemmer = PorterStemmer()
        tokenized_words = []
        set_of_link_titles = []

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
                if link_title not in set_of_link_titles:
                    set_of_link_titles.append(link_title)
            else:
                word = word.lower()
                if word not in STOP_WORDS:
                    tokenized_words.append(nltk_stemmer.stem(word))
        
        return(tokenized_words, set_of_link_titles)

    def make_title_dict(self):
        for page in self.all_pages:
            id: int = int(page.find("id").text)
            title: str = page.find('title').text
            self.id_to_title_dict[id] = title
            self.title_to_id_dict[title] = id
        write_title_file(self.title_file, self.id_to_title_dict)

    def make_word_dict(self):
        words_to_id_tf = {}
        id_to_max_count = {}

        for page in self.all_pages:
            text: str = page.find("text").text
            id: int = int(page.find("id").text)
            # all_words = re.findall(n_regex, text)
            # all_words is a list of tokenize/stemmed/stopped words for a given page
            all_words_in_page = self.tokenize_stop_stem(text)[0]
            links_set = self.tokenize_stop_stem(text)[1]
            self.page_to_links[id] = links_set

            max_count = 0
            

            for word in all_words_in_page: 
                if word not in self.words_to_id_to_count:
                    # add id first
                    self.words_to_id_to_count[word]= {id:1}
                    # might cause problem w diff ids idk tho
                else:
                    if id not in self.words_to_id_to_count[word].keys():
                        self.words_to_id_to_count[word][id] = 1
                    else:
                        self.words_to_id_to_count[word][id] += 1
                
                if self.words_to_id_to_count[word][id] > max_count:
                    max_count = self.words_to_id_to_count[word][id]
    
            id_to_max_count[id] = max_count 
            # go through page: to find raw freq & max count, again to calc tf
        
        
        for word in self.words_to_id_to_count.keys():
            for id in self.words_to_id_to_count[word].keys():
                if word not in words_to_id_tf:
                    words_to_id_tf[word]= {id:(self.words_to_id_to_count[word][id]) / id_to_max_count[id]}
                else:
                    words_to_id_tf[word][id] = (self.words_to_id_to_count[word][id]) / id_to_max_count[id]

        
        words_to_idf = {}

        
        for word in self.words_to_id_to_count.keys():
            n_i = len(self.words_to_id_to_count[word])
            # if word not in words_to_idf:
            words_to_idf[word] = math.log(self.n/n_i)

        
        for word in self.words_to_id_to_count.keys():
            for id in self.words_to_id_to_count[word].keys():
                if word not in self.word_dict:
                    self.word_dict[word] = {id : words_to_id_tf[word][id] * words_to_idf[word]}
                else: 
                    self.word_dict[word][id] = words_to_id_tf[word][id] * words_to_idf[word]
        write_words_file(self.word_file, self.word_dict)

    def make_id_to_link_dict(self):
        for id in self.page_to_links:
            linked_ids = []
            for title in self.page_to_links[id]:
                if title not in linked_ids:
                    linked_ids.append(self.title_to_id_dict[title])
            print(linked_ids)
            self.id_to_linked_ids[id] = linked_ids

    def make_doc_dict(self):
        self.fill_rank_dicts()
        
        while self.distance(self.old_rank_dict, self.new_rank_dict) > 0.001:
            self.old_rank_dict = self.new_rank_dict
            for to_id in self.id_to_title_dict.keys():
                self.new_rank_dict[to_id] = 0
                for from_id in self.id_to_title_dict.keys():
                    self.new_rank_dict[to_id] += (self.weight_dict[from_id][to_id] * self.old_rank_dict[from_id])
        
        self.doc_dict = self.new_rank_dict

        write_docs_file(self.doc_file, self.doc_dict)
    
    def weight_calculator(self):
        for from_id in self.id_to_title_dict.keys():
            if len(self.id_to_linked_ids[from_id]) == 0:
                link_count = self.n -1
            elif len(self.id_to_linked_ids[from_id]) == 1 and id in self.id_to_linked_ids[from_id]:
                link_count = self.n -1
            else:
                link_count = len(self.id_to_linked_ids[from_id])
                if id in self.id_to_linked_ids[from_id] and len(self.id_to_linked_ids[from_id]) > 1:
                    link_count -= 1
            to_id_weight = {}

            for to_id in self.id_to_title_dict.keys():
                if from_id == to_id:
                    weight = 0.15/self.n
                elif to_id in self.id_to_linked_ids[from_id]:
                    weight = (0.15/self.n) + (0.85/link_count)
                elif link_count == self.n - 1:
                    weight = (0.15/self.n) + (0.85/link_count)
                else:
                    weight = 0.15/self.n
                to_id_weight[to_id] = weight
            
            self.weight_dict[from_id] = to_id_weight

    def distance(self, old_rank, new_rank):
        total_distance = 0 
        for id in self.id_to_title_dict.keys():
            total_distance += (old_rank[id] - new_rank[id]) ** 2
        return total_distance ** 1/2

    def fill_rank_dicts(self):
        for id in self.id_to_title_dict.keys():
            self.old_rank_dict[id] = 0
            self.new_rank_dict[id] = 1/self.n
    


            




    
    



        
        

                 

if __name__ == "__main__":
    my_indexer = Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])