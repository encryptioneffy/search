# search-encryptioneffy-jessicaliu526
encryptioneffy-jessicaliu526 team's search repo

Query Edge Cases Tests
(after running python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word" in the terminal)
1) no input with page rank

INPUT:
python3 query.py "--pagerank" "title" "doc" "word" in the terminal
after the ">>search" appears, press enter
RETURNED: 
try-catch excpetion msg "please do not leave the search query blank"

2) all stop words
--> returns nothing / try-catch exception msg

INPUT:
python3 query.py "title" "doc" "word" in the terminal
after the ">>search" appears, type "a the of in" and press enter
RETURNED:
try-catch exception msg "please include non-stop words in your query"

3) one stop word
--> returns nothing / try-catch exception msg

INPUT:
python3 query.py "title" "doc" "word" in the terminal
after the ">>search" appears, type "the" and press enter
RETURNED:
try-catch exception msg "please include non-stop words in your query"


4) all variations of the same stem words VS all the same stem word
--> both will return the same top 10 list

INPUT(2):
python3 query.py "title" "doc" "word" in the terminal
after the ">>search" appears, type "cut cutting" and press enter

python3 query.py "title" "doc" "word" in the terminal
after the ">>search" appears, type "cut cut" and press enter

RETURNED:
Both the "cut cutting" and "cut cut" queries returns the same top 10 list.

5) one 'mispelled' stem word
--> returns pages that contain non-stemmed version of that word

INPUT:
python3 query.py "title" "doc" "word" in the terminal
after the ">>search" appears, type "cheesi" and press enter
RETURNED:
try-catch exception msg "please include non-stop words in your query"

6) weird capitalization VS normal capitalization
--> both will return the same top 10 list

7) something that appears many many times on one low authority page (query w/ page rank)
--> that one low-authority page will not be part of top 10

8) all words that are not in corpus
--> return try/catch exception message

9) some words not in corpus, some words are in corpus
--> ignores the non-corpus words

10) words that appear on fewer than 10 pages in the corpus
--> returns only the pages that contain that word

Query Basic Cases Tests
1) one word query
2) multi-word query
3) one word query with page rank
4) one word query without page rank
5) multi-word query with page rank
6) multi-word query without page rank

SysArg Tests

