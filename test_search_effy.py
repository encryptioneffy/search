# # parsing
# # tokenizing
# """ 1. make sure titles are being tokenized like text
# 2. all the different link tokenizing scenarios
# 3. tokenizing basic text (no links) """
# # ids to link ids data structure
from index import *
import pytest
from pytest import approx

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

