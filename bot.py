#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TELEGRAM_TOKEN = "123:your-bot-token"
EXCHANGE_URL = 'https://query.yahooapis.com/v1/public/yql?q=select+*+from+yahoo.finance.xchange+where+pair+=+"USDRUB,EURRUB,BTCUSD"&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='
JOKE_URL = "http://www.umori.li/api/get?site=bash.im&name=bash&num=1"
CHAT_ID = -62654714
BOOBS_API_URL = "http://api.oboobs.ru/noise/1/"
BOOBS_MEDIA_URL = "http://media.oboobs.ru/"
BEER_URL = "http://www.sexypictures.dk/images/Biertje.jpg"


from telegram import Updater
import logging
import telegram
import requests
import json
import random
import re


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Привет, овощи!")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Сам себе помоги!")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def echo(bot, update):
    if (checkWords(update.message.text, [u"хуй", u"охуеть", u"хуясе", u"хуевый", u"хуевина", u"хуета", u"хуйца"])):
        bot.sendMessage(update.message.chat_id, text="Заебал материться, пидорас шерстяной!")

    if (checkWords(update.message.text, [u"курс", u"курсы", u"доллар", u"бакс", u"евро", u"биток", u"биткоин"])):
        r = requests.get(EXCHANGE_URL)
        json = r.json()
        result = "Курсы:\n$ - " + str(json["query"]["results"]["rate"][0]["Rate"]) + " руб.\n" + "€ - " + str(json["query"]["results"]["rate"][1]["Rate"]) + " руб.\n" + "BTC - " + str(json["query"]["results"]["rate"][2]["Rate"]) + " USD"
        bot.sendMessage(update.message.chat_id, text=result)

    if (checkWords(update.message.text, [u"шутка", u"шутеечка", u"шуточка", u"прикол", u"ржака"])):
        r = requests.get(JOKE_URL + "00")
        json = r.json()
        bot.sendMessage(update.message.chat_id, text=re.sub('<[^<]+?>', '', json[random.randrange(0, 101, 2)]["elementPureHtml"]))

    if (checkWords(update.message.text, [u"сиськи", u"сиська", u"сисяндра", u"сиси", u"сисю", u"булки", u"буфера"])):
        r = requests.get(BOOBS_API_URL)
        json = r.json()
        bot.sendPhoto(chat_id=update.message.chat_id, photo=BOOBS_MEDIA_URL + "/" + json[0]["preview"])

    if (checkWords(update.message.text, [u"пиво", u"пивко", u"пивас", u"пиву", u"пива", u"пивку", u"пивасику"])):
        bot.sendPhoto(chat_id=update.message.chat_id, photo=BEER_URL)


def jobJoke(bot):
    r = requests.get(JOKE_URL)
    json = r.json()
    bot.sendMessage(CHAT_ID, text=re.sub('<[^<]+?>', '', json[0]["elementPureHtml"]))


def checkWords(message, targetWords):
    messageWords = re.sub("[!?.;:()]", " ", message.lower()).split(" ")
    intersectWords = set(messageWords).intersection(targetWords)
    return True if len(intersectWords) > 0 else False


def main():
    global job_queue
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
 
    dp.addTelegramMessageHandler(echo)

    dp.addErrorHandler(error)

    updater.job_queue.put(jobJoke, 28800, repeat=True)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
