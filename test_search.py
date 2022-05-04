from hashlib import new
from index import *
import pytest
from pytest import approx

def test_tf_idf_pagerank_distance_maxcount_relevance():
    index1 = Index("wikis/test1.xml", "title", "doc", "word")

    index1.make_word_dict()

#testing tf values
    assert index1.words_to_id_tf["woof"][1] == 1.0
    assert index1.words_to_id_tf["woof"][4] == 0.5
    assert index1.words_to_id_tf["dog"][2] == 1.0
    assert index1.words_to_id_tf["chees"][2] == 1.0
    assert index1.words_to_id_tf["bark"][1] == 1.0
    assert index1.words_to_id_tf["bit"][3] == 0.5
    assert index1.words_to_id_tf["run"][3] == 0.5
#testing idf values
    #zero because woof is in every page!
    assert index1.words_to_idf["woof"] == 0.0
    assert index1.words_to_idf["chees"] == 0.22314355131420976
    assert index1.words_to_idf["run"] == 0.9162907318741551
    assert index1.words_to_idf["bark"] == 1.6094379124341003
    assert index1.words_to_idf["bit"] == 0.5108256237659907
#testing max count
    assert index1.id_to_max_count[1] == 2
    assert index1.id_to_max_count[2] == 2
    assert index1.id_to_max_count[3] == 4
    assert index1.id_to_max_count[4] == 4
    assert index1.id_to_max_count[5] == 4
#testing relevance
    #zero because woof is in every page!
    assert index1.word_dict["woof"][1] == 0.0 
    assert index1.word_dict["bark"][1] == 1.6094379124341003 
    assert index1.word_dict["pug"][1] == 1.6094379124341003
    assert index1.word_dict["dog"][2] == 1.6094379124341003
    assert index1.word_dict["ate"][2] == 1.6094379124341003
    assert index1.word_dict["chees"][3] == 0.22314355131420976
    assert index1.word_dict["run"][3] == 0.45814536593707755
    assert index1.word_dict["run"][4] == 0.9162907318741551 
    assert index1.word_dict["bit"][3] == 0.25541281188299536

#testing weight calculations
    index1.weight_calculator()

    assert index1.weight_dict[1][1] == 0.03
    assert index1.weight_dict[1][3] == 0.2425
    assert index1.weight_dict[2][1] == 0.88
    assert index1.weight_dict[2][5] == 0.03
    assert index1.weight_dict[3][3] == 0.03
    assert index1.weight_dict[4][3] == 0.88
    assert index1.weight_dict[5][3] == 0.88

#creating index objects with the page rank examples
    page_rank_1 = Index("wikis/PageRankExample1.xml", "title", "doc", "word")
    page_rank_1.make_doc_dict()

    page_rank_2 = Index("wikis/PageRankExample2.xml", "title", "doc", "word")
    page_rank_2.make_doc_dict()

    page_rank_3 = Index("wikis/PageRankExample3.xml", "title", "doc", "word")
    page_rank_3.make_doc_dict()

    page_rank_4 = Index("wikis/PageRankExample4.xml", "title", "doc", "word")
    page_rank_4.make_doc_dict()

#testing pagerank1
    assert page_rank_1.doc_dict[1] == 0.4326427188659158
    assert page_rank_1.doc_dict[2] == 0.23402394780075067
    assert page_rank_1.doc_dict[3] == 0.33333333333333326
#testing page rank 2
    assert page_rank_2.doc_dict[1] == 0.20184346250214996
    assert page_rank_2.doc_dict[2] == 0.03749999999999998
    assert page_rank_2.doc_dict[3] == 0.37396603749279056
    assert page_rank_2.doc_dict[4] == 0.3866905000050588
#testing page rank 3
    assert page_rank_3.doc_dict[1] == 0.05242784862611451
    assert page_rank_3.doc_dict[2] == 0.05242784862611451
    assert page_rank_3.doc_dict[3] == 0.4475721513738852
    assert page_rank_3.doc_dict[4] == 0.44757215137388523
#testing page rank 4
    assert page_rank_4.doc_dict[1] == 0.0375
    assert page_rank_4.doc_dict[2] == 0.0375
    assert page_rank_4.doc_dict[3] == 0.46249999999999997
    assert page_rank_4.doc_dict[4] == 0.4624999999999999

#testing distance helper
    old_rank = {1:0, 2:0, 3:0, 4:0, 5:0}
    new_rank = {1:0.2, 2:0.2, 3:0.2, 4:0.2, 5:0.2}
    assert index1.distance(old_rank, new_rank) == 0.447213595499958

def test_parsing_xml():
    """ Testing that the XML file is parsed correctly, and that the 
    individual title, id, and text sections of the parsed XML file are 
    being parsed correctly via make_title_dict(self) helper function in 
    index.py"""
    index2 = Index("wikis/test_tf_idf.xml", "title", "doc", "word")
    assert len(index2.all_pages) == 3
    assert len(index2.id_to_title_dict.keys()) == 3
    assert index2.id_to_title_dict[1] == "Page 1"
    assert index2.id_to_title_dict[2] == "Page 2"
    assert index2.id_to_title_dict[3] == "Page 3"

    """.all_pages[0].find("text").text.strip() is in our index clss 
    but we store it as a variable for each page so we did not make
    it an instance variable"""
    assert index2.all_pages[0].find("text").text.strip() == "the dog bit the man"
    assert index2.all_pages[1].find("text").text.strip() == "the dog ate cheese"
    assert index2.all_pages[2].find("text").text.strip() == "the cheese bit the cheese"
    # assert that the title & id & text are extracted properly?

def test_tokenize_stopping_and_stemming():
    ''' 
    Note: tokenizing, stop, and stem are all done in 1 helper function

    Tokenizing, Stops, and Stems the 4 different types of links
    1. One-word | One-word pipelinks
    2. One-word text links
    3. Multi-word links
    4. Multi-word pipelinks
    '''
    text1 = "Hey! My name is EFfy and I like [[Sharks|Hammerheads]]. \
        I do NOT like [[Whale]] [[Sharks]]. By the way, Mom asked \
            [[How are you?]]. She is worried worry about the \
                [[Presidents|Losing Money]]. Now we are stemming some \
                    cheesy, running, and funny English word words. \
                        Going to sleep sleeps slept sleeping."
    index1 = Index("wikis/test_tf_idf.xml", "title", "doc", "word")
    list1 = ['hey','name','effi','like','hammerhead','like',\
        'whale','shark','way','mom','ask','worri','worri','lose','money',\
            'stem','cheesi','run','funni','english','word','word','go',\
                'sleep','sleep','slept','sleep']
    list2 = ['Sharks', 'Whale', 'How are you?', 'Presidents']
    assert index1.tokenize_stop_stem(text1)[0] == list1
    assert index1.tokenize_stop_stem(text1)[1] == list2

def test_storing_links():
    """ Testing the def make_id_to_link_dict(self) helper function"""
    index2 = Index("wikis/test2.xml", "title", "doc", "word")
    index2.make_id_to_link_dict

    assert index2.id_to_linked_ids[1] == [2, 5]
    assert index2.id_to_linked_ids[2] == [1, 4]
    assert index2.id_to_linked_ids[3] == [4]
    assert index2.id_to_linked_ids[4] == [4]
    assert index2.id_to_linked_ids[5] == []

def test_tokenize_stopping_and_stemming():
    ''' 
    Testing the tokenizing, stopping, and stemming of text containing
    4 different types of links
        1. One-word | One-word pipelinks
        2. One-word text links
        3. Multi-word text links
        4. Multi-word pipelinks
    
    Note: tokenizing, stop, and stem are all done in the same helper function
    '''
    text1 = "Hey! My name is EFfy and I like [[Sharks|Hammerheads]]. \
        I do NOT like [[Whale]] [[Sharks]]. By the way, Mom asked \
            [[How are you?]]. She is worried worry about the \
                [[Presidents|Losing Money]]. Now we are stemming some \
                    cheesy, running, and funny English word words. \
                        Going to sleep sleeps slept sleeping."
    index1 = Index("wikis/test_tf_idf.xml", "title", "doc", "word")
    list1 = ['hey','name','effi','like','hammerhead','like',\
        'whale','shark','way','mom','ask','worri','worri','lose','money',\
            'stem','cheesi','run','funni','english','word','word','go',\
                'sleep','sleep','slept','sleep']
    list2 = ['Sharks', 'Whale', 'How are you?', 'Presidents']
    assert index1.tokenize_stop_stem(text1)[0] == list1
    assert index1.tokenize_stop_stem(text1)[1] == list2

def test_storing_links():
    """ Testing the def make_id_to_link_dict(self) helper function"""
    index2 = Index("wikis/test2.xml", "title", "doc", "word")
    index2.make_id_to_link_dict

    assert index2.id_to_linked_ids[1] == [2, 5]
    assert index2.id_to_linked_ids[2] == [1, 4]
    assert index2.id_to_linked_ids[3] == [4]
    assert index2.id_to_linked_ids[4] == [4]
    assert index2.id_to_linked_ids[5] == []




    







