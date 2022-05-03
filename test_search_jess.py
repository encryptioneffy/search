from hashlib import new
from index import *
import pytest

def test_tf_idf_pagerank():
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



    







