from index import *
import pytest

def test_tf_idf_pagerank():
    index1 = Index("wikis/test1.xml", "title", "doc", "word")

    index1.make_word_dict()

#testing tf values
    assert index1.words_to_id_tf["woof"][1] == 1.0
    assert index1.words_to_id_tf["dog"][2] == 1.0
    assert index1.words_to_id_tf["run"][3] == 0.5
#testing idf values
    assert index1.words_to_idf["woof"] == 0.0
    assert index1.words_to_idf["chees"] == 0.22314355131420976
    assert index1.words_to_idf["run"] == 0.9162907318741551
#testing max count
    assert index1.id_to_max_count[1] == 2
    assert index1.id_to_max_count[2] == 2
    assert index1.id_to_max_count[3] == 4
    assert index1.id_to_max_count[4] == 4
    assert index1.id_to_max_count[5] == 4







