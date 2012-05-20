# -*- coding: utf-8 -*-
from re import sub
from oice.langdet import langdet

def encoding_sucks(text):
    try:
        return text.encode("Utf-8")
    except UnicodeError:
        pass
    try:
        return text.decode("Utf-8")
    except UnicodeDecodeError:
        pass
    try:
        return text.encode("iso-8859-1")
    except:
        pass
    try:
        return text.decode("iso-8859-1")
    except:
        pass
    return "could not get the title :(, tell Bram that this website sucks"

def get_langue_from_html(text):
    text = sub("[^\w ]", lambda x: "", text)
    lang = langdet.LanguageDetector.detect(text).iso.upper()
    if lang in ('FR', 'EN', 'ES'):
        return lang

def format_site_from_url(url):
    return ".".join(map(lambda x: x.capitalize(), url.split("/")[2].replace("www.", "").split(".")[:-1]))

def clean_title(title):
    choose_biggest = lambda choices: max(choices, key=lambda x: len(x))
    title = encoding_sucks(title)
    title = choose_biggest(title.split(" - "))
    title = choose_biggest(title.split(" | "))
    title = choose_biggest(title.split(" ["))
    title = choose_biggest(title.split(u" « "))
    title = choose_biggest(title.split(u" – "))
    return title
