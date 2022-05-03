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







