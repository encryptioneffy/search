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
    index2 = Index("wikis/test_tf_idf.xml", "title", "doc", "word")
    assert len(index2.all_pages) == 3
    assert len(index2.id_to_title_dict.keys()) == 3
    assert index2.id_to_title_dict[1] == "Page 1"
    assert index2.id_to_title_dict[2] == "Page 2"
    assert index2.id_to_title_dict[3] == "Page 3"
    assert index2.all_pages[0].find("text").text == "the dog bit the man"
    assert index2.all_pages[1].find("text").text == "the dog ate cheese"
    assert index2.all_pages[2].find("text").text == "the cheese bit the cheese"
    # assert that the title & id & text are extracted properly?
