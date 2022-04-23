import sys
import xml.etree.ElementTree as et

root: Element = et.parse(<xml filepath>).getroot()

all_pages: ElementTree = root.findall("page")

id: int = page.find("id").text
title: str = page.find('title').text

def write_title_file(dict: self.title_file):
    for page in all_pages:
        id: int = page.find("id").text
        title: str = page.find('title').text
        self.title_file[id] = title

    wr

# sys.argv = 1, 2, 3

# print(sys.argv)
