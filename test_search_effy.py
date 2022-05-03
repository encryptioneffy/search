# # parsing
# # tokenizing
# """ 1. make sure titles are being tokenized like text
# 2. all the different link tokenizing scenarios
# 3. tokenizing basic text (no links) """
# # ids to link ids data structure
# import index
# from index import *
# import pytest
# from pytest import approx

# def test_parsing_xml():
#     indexer_ex = Indexer("wikis/test_tf_idf.xml", "title", "doc", "word")
#     assert len(indexer_ex.all_pages) == 3
#     # assert that the title & id & text are extracted properly?
