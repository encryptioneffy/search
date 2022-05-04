# search-encryptioneffy-jessicaliu526
encryptioneffy-jessicaliu526 team's search repo

Query Edge Cases 
* after doing running python3 index.py "wikis\SmallWiki.xml" "title" "doc" "word" in the terminal
1) no input with page rank

WE INPUTTED:
- python3 query.py "--pagerank" "title" "doc" "word" in the terminal
- after the ">>search" appears, press enter
RETURNED: 
- try-catch excpetion msg "please do not leave the search query blank"

2) no input without page rank


3) all stop words
--> returns nothing / try-catch exception msg

4) one stop word
--> returns nothing / try-catch exception msg

5) all variations of the same stem words VS all the same stem word
--> will return the same top 10 list

10) one stem word
11) different capitalization
12) something that appears multiple times on a page
13) all words that are not in corpus
14) some words not in corpus, some words are in corpus

Query Basic Cases
