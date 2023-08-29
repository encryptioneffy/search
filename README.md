# Search
- Type: Backend Project
- Status: Completed

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
  python3 query.py "title" "doc" "word"
  after the ">>search" appears, type "a the of in" and press enter
  RETURNED:
  try-catch exception msg "please enter non-stop words in your query"

3) one stop word
--> return try/catch exception message

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word"
  after the ">>search" appears, type "the" and press enter
  RETURNED:
  try-catch exception msg "please enter non-stop words in your query"


4) all variations of the same stem words VS. all the same stem word
--> both queries will return the same top 10 list

  INPUT(2):
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" 
  after the ">>search" appears, type "cut cutting" and press enter
  after the ">>search" appears again, type "cut cut" and press enter
  RETURNED:
  Both the "cut cutting" and "cut cut" queries returns the same following top 10 list.
  ['The Seven Hills', 'Byrsa', 'Salammb?', 'Motya', 'History of Carthage', 'Anachronism', 'Ancient Carthage', 'Carthage', 'Philosophy of war', 'Macro-historical']

5) one 'mispelled' stem word
--> returns pages that contain non-stemmed version of that word

  INPUT:
  python3 index.py "wikis\test3.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" 
  after the ">>search" appears, type "cheesi" and press enter
  RETURNED:
  top pages that contain variations of the stem word cheesi, such as "cheesiest" and "cheesy"
  ['woof', 'a']

6) weird capitalization VS. normal capitalization
--> both will return the same top 10 list

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" 
  after the ">>search" appears, type "wOrLd WAR" and press enter
  after the ">>search" appears again, type "world war" and press enter
  RETURNED:
  Both the "wOrLd WAR" and "world war" queries returns the same following top 10 list.
  ['Philosophy of war', 'List of wartime cross-dressers', 'Effects of war', 'Progressive war', 'War referendum', 'War profiteering', 'War', 'Theater (warfare)', 'War porn', 'Military history']

7) something that appears many many times on one low authority page (query w/ page rank)
--> that low-authority page will not be part of top 10

  INPUT:
  python3 index.py "wikis\test4.xml" "title" "doc" "word" (in this wiki, all pages are being linked to, except for page of id 5 titled "Fake News")
  python3 query.py "--pagerank" "title" "doc" "word" in the terminal
  after the ">>search" appears, type "Kim" and press enter
  RETURNED:
  The 10 pages in the wiki that are being linked to/have some authority and containing "Kim is fine" in the text.
  That low-authority page in the wiki (which no pages link to) titled "Fake News" and containing "Kim is pregnant!!!" in the text will not appear in this top 10 list. ['C', 'G', 'I', 'A', 'B', 'D', 'K', 'F', 'H', 'J']

8) all words that are not in corpus
--> return empty list

  INPUT:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "title" "doc" "word" in the terminal
  after the ">>search" appears, type "funky junky jacket" and press enter
  RETURNED:
  empty list bc no pages contain query words []


9) some words not in corpus, some words are in corpus 
--> ignores the non-corpus words. When we compare the top 10 list to the same query with the non-corpus words NOT included, the top 10 lists will be the same.

  INPUTTED:
  python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word"
  python3 query.py "--pagerank" "title" "doc" "word" in the terminal
  after the ">>search" appears, type "funky english war" and press enter
  after the ">>search" appears again, type "english war" and press enter
  RETURNED:
  Both the "funky english war" and "english war" queries returns the same following top 10 list.
  ['Carthage', 'Utica, Tunisia', 'Civilian casualty ratio', 'Loss exchange ratio', 'Byrsa', 'War', 'Military history', 'Germany', 'Rome', 'Battle of Carthage (698)']


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
INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word"
python3 query.py "title" "doc" "word"
after the ">>search" appears, type "economy" and press enter
RETURNED:
['Economy of the Faroe Islands', 'Economy of Malta', 'Economy of Guadeloupe', 'Economy of North Korea', 'Post-communism', 'Economy of Montserrat', 'Economy of Kazakhstan', 'Economy of Hong Kong', 'Telecommunications in Mauritania', 'Economy of Finland']

2) multi-word query
INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word"
python3 query.py "title" "doc" "word"
after the ">>search" appears, type "Queer of England" and press enter
RETURNED:
['New England (disambiguation)', 'LMS', 'New England Patriots', 'John Wycliffe', 'Pope Alexander IV', 'Henry VII of England', 'Lammas', 'Kent', 'John Ambrose Fleming', 'Luddite']

3) one word query with page rank
INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word"
python3 query.py --pagerank "title" "doc" "word"
after the ">>search" appears, type "pollution" and press enter
RETURNED:
['Islamabad Capital Territory', 'Geography of Hungary', 'Nigeria', 'Lake Michigan', 'North Africa', 'Pakistan', 'Portugal', 'Geography of Morocco', 'Houston', 'Nazi Germany']


4) one word query without page rank
INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word"
python3 query.py "title" "doc" "word"
after the ">>search" appears, type "pollution" and press enter
RETURNED:
['Geography of Hungary', 'Geography of Morocco', 'Geography of Peru', 'Geography of Nicaragua', 'Geography of Kenya', 'Geography of Lebanon', 'Military of Latvia', 'Lazio', 'Microeconomics', 'Islamabad Capital Territory']

5) multi-word query with page rank
INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word"
python3 query.py --pagerank "title" "doc" "word"
after the ">>search" appears, type "oil pollution middle east" and press enter
RETURNED:
['Neolithic', 'Northern Hemisphere', 'Netherlands', 'Pakistan', 'Islamabad Capital Territory', 'History of the Netherlands', 'Great Schism', 'Harappa', 'New Amsterdam', 'Niger']

6) multi-word query without page rank
INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word"
python3 query.py "title" "doc" "word"
after the ">>search" appears, type "oil pollution middle east" and press enter
RETURNED:
['Imperialism in Asia', 'East Slavic languages', 'Great Schism', 'Kent', 'History of Lebanon', 'West Low German', 'Nassau, Bahamas', 'Northern Hemisphere', 'Lower Mainland', 'Geography of Kenya']



SysArg Tests
1) index fewer than 5 sysargs given

INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc"
RETURNED:
print message 'invalid number of inputs'

2) index more than 5 sysargs given

INPUT:
python3 index.py "wikis\MedWiki.xml" "title" "doc" "word" "rando"
RETURNED:
print message 'invalid number of inputs'

3) query more than 5 sysargs given

INPUT:
python3 query.py --pagerank "title" "doc" "word" "rando"
RETURNED:
print message 'invalid number of inputs'

4) query fewer than 5 sysargs given

INPUT:
python3 query.py "doc" "word" 
RETURNED:
print message 'invalid number of inputs'

5) no sysargs were given following python3 index.py 

INPUT:
python3 index.py
RETURNED:
print message 'invalid number of inputs'

6) no sysargs were given following python3 query.py

INPUT:
python3 query.py
RETURNED:
print message 'invalid number of inputs'

7) invalid xml filepath sysarg for python3 index.py

INPUT:
python3 index.py "nonexistentXMLfile" "title" "doc" "word"
RETURNED:
print message 'invalid xml file path'

8) wrong filepath sysargs for python3 query,py

INPUT: 
python3 query.py "title" "doc" "filethatdoesnotexist" "word"
RETURNED:
print message 'invalid file paths'


INPUT:
python3 query.py --pagerank "title" "doc" "nonexistentfile" 
RETURNED:
print message 'invalid file paths'

INPUT:
python3 query.py "nonexistentfile" "doc" "word"
RETURNED:
print message 'invalid file paths'
