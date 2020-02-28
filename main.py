from bs4 import BeautifulSoup
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import urllib.request
import sys

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def scrape_download_link(book_name):
    book_format = "pdf"

    url = "http://libgen.is/search.php?req=" + "+".join(
        book_name.split()) + "&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"

    soup = BeautifulSoup(urllib.request.urlopen(url))

    def get_href(raw_td):
        raw_td = str(raw_td)
        start_index = raw_td.find("http:")
        end_index = raw_td[start_index:].find("\"") + start_index
        return raw_td[start_index:end_index]

    for tr in soup.find_all('tr')[3:]:
        tds = tr.find_all('td')

        if len(tds) < 10:
            continue

        # if not author_name.lower() in str(tds[1].text).lower():
            # continue

        if not book_name.lower() in str(tds[2].text).lower():
            continue

        if tds[8].text != book_format:
            continue

        next_page = get_href(tds[10])
        soup = BeautifulSoup(urllib.request.urlopen(next_page))
        for link in soup.find_all('a'):
            return link['href']

    return "unfortunately we didn't found the book ... maybe you didn't write the name correctly?"


def get_link(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="searching for your book")
    context.bot.send_message(chat_id=update.effective_chat.id, text=scrape_download_link(update.message.text))


def main():
    updater = Updater(token=sys.argv[1], use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    download_handler = MessageHandler(Filters.text, get_link)
    dispatcher.add_handler(download_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
