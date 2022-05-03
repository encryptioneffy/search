from index import *
import pytest

index1 = Index("wikis/test_tf_idf.xml", "title", "doc", "word")

index1.make_word_dict()


assert index1.words_to_id_tf["woof"][1] == 1.0
assert index1.words_to_id_tf["dog"][2] == 1.0
assert index1.words_to_id_tf["run"][3] == 0.5

assert index1.words_to_idf["woof"] == 0.0
assert index1.words_to_idf["chees"] == 0.22314355131420976
assert index1.words_to_idf["run"] == 0.9162907318741551

assert index1.id_to_max_count[1] == 1
assert index1.id_to_max_count[2] == 1
assert index1.id_to_max_count[3] == 2
assert index1.id_to_max_count[4] == 2
assert index1.id_to_max_count[5] == 2






