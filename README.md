# search-encryptioneffy-jessicaliu526
encryptioneffy-jessicaliu526 team's search repo

Query Edge Cases Tests
1) no input with page rank
--> return try/catch exception message

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "--pagerank" "title" "doc" "word"
  after the ">>search" appears, press enter
  RETURNED: 
  try-catch excpetion msg "please do not leave the search query blank"

2) all stop words
--> return try/catch exception message

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "a the of in" and press enter
  RETURNED:
  try-catch exception msg "please include non-stop words in your query"

3) one stop word
--> return try/catch exception message

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "the" and press enter
  RETURNED:
  try-catch exception msg "please include non-stop words in your query"


4) all variations of the same stem words VS. all the same stem word
--> both queries will return the same top 10 list

  INPUT(2):
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "cut cutting" and press enter
  after the ">>search" appears again, type "cut cut" and press enter
  RETURNED:
  Both the "cut cutting" and "cut cut" queries returns the same following top 10 list.

5) one 'mispelled' stem word
--> returns pages that contain non-stemmed version of that word

  INPUT:
  python3 index.py "wikis\test3.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "cheesi" and press enter
  RETURNED:
  top pages that contain variations of the stem word cheesi, such as "cheese" "cheesiest" and "cheesy"

6) weird capitalization VS. normal capitalization
--> both will return the same top 10 list

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "wOrLd WAR" and press enter
  after the ">>search" appears again, type "world war" and press enter
  RETURNED:
  Both the "wOrLd WAR" and "world war" queries returns the same following top 10 list.

7) something that appears many many times on one low authority page (query w/ page rank)
--> that low-authority page will not be part of top 10

  INPUT:
  python3 index.py "wikis\test4.xml" "title" "doc" "word" (in this wiki, all pages are being linked to, except for page of id 5 titled "Fake News")
  python3 query.py "--pagerank" "title" "doc" "word" in the terminal
  after the ">>search" appears, type "Kim" and press enter
  RETURNED:
  The 10 pages in the wiki that are being linked to/have some authority and containing "Kim is fine" in the text.
  That low-authority page in the wiki (which no pages link to) titled "Fake News" and containing "Kim is pregnant!!!" in the text will not appear in this top 10 list.

8) all words that are not in corpus
--> return try/catch exception message

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "funky junky jacket" and press enter
  RETURNED:
  try-catch exception msg "no pages containing query terms were found"


9) some words not in corpus, some words are in corpus 
--> ignores the non-corpus words. When we compare the top 10 list to the same query with the non-corpus words NOT included, the top 10 lists will be the same.

  INPUTTED:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "funky english war" and press enter
  after the ">>search" appears again, type "english war" and press enter
  RETURNED:
  Both the "funky english war" and "english war" queries returns the same following top 10 list.

10) words that appear on fewer than 10 pages in the corpus
--> returns only the pages that contain that word

  INPUT: 
  python3 index.py "wikis\test_tf_idf.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "dog" and press enter
  RETURNED:
  Since only 2 of the 3 pages contain the word dog, only those pages will be included in the top 10 list. Page 3 will not be returned in top 10 list.
  [Page 1, Page 2]


Query Basic Cases Tests
1) one word query
3) multi-word query
4) one word query with page rank
5) one word query without page rank
6) multi-word query with page rank
7) multi-word query without page rank

SysArg Tests
1) fewer than 4 sysargs given
2) more than 4/5 sysargs given
3) no sysargs were given following python2 index.py / python2 query.py
4) incorrect filepaths given for index.py
5) incorrect filepaths given for query.py

