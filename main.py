from bs4 import BeautifulSoup
import csv
from urllib import request
import sys

book_name = str(input("enter the book name->"))
author_name = input("enter the author name->")
book_format = input("enter the book format(pdf/djvu/epub)->")

url = "http://libgen.is/search.php?req=" + "+".join(book_name.split()) + "&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"

soup = BeautifulSoup(request.urlopen(url))


def get_href(raw_td):
    raw_td = str(raw_td)
    start_index = raw_td.find("http:")
    end_index = raw_td[start_index:].find("\"") + start_index
    return raw_td[start_index:end_index]


for tr in soup.find_all('tr')[3:]:
    tds = tr.find_all('td')

    if len(tds) < 10:
        continue

    if not author_name.lower() in str(tds[1].text).lower():
        continue

    if not book_name.lower() in str(tds[2].text).lower():
        continue

    if tds[8].text != book_format:
        continue

    next_page = get_href(tds[10])
    soup = BeautifulSoup(request.urlopen(next_page))
    for link in soup.find_all('a'):
        if link['href'] and 'md5' in link['href']:
            print(link['href'])
            sys.exit()

print("unfortunately we didn't found the book you wanted . maybe you wrote the wrong info, or you can try again with "
      "different format")
