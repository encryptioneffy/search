# search-encryptioneffy-jessicaliu526
encryptioneffy-jessicaliu526 team's search repo

Query Edge Cases 
(after running python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word" in the terminal)
1) no input with page rank

INPUT:
python3 query.py "--pagerank" "title" "doc" "word" in the terminal
after the ">>search" appears, press enter
RETURNED: 
try-catch excpetion msg "please do not leave the search query blank"

2) all stop words
--> returns nothing / try-catch exception msg

3) one stop word
--> returns nothing / try-catch exception msg

4) all variations of the same stem words VS all the same stem word
--> both will return the same top 10 list

5) one 'mispelled' stem word
--> returns pages that contain non-stemmed version of that word

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

Query Basic Cases
