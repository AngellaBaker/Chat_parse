import json
import re
from bs4 import BeautifulSoup
import urllib2

def parse_mentions(chat_str):
    return re.findall(r'\B@([A-Za-z0-9]+)', chat_str)

def parse_emoticons(chat_str):
    return re.findall(r'\((.*?)\)', chat_str)

def parse_urls(chat_str):
    url = re.findall(r'https?://[^\s<>,"]+|www\.[^\s<>,"]+', chat_str)
    links_list = []
    for i in url:
        url_dict = {}
        url_dict["url"] = i
        if 'http' not in i:
            page = urllib2.urlopen('http://' + i)
        else:
            page = urllib2.urlopen(i, None, 5)
        try:
            url_dict["title"] = BeautifulSoup(page.read()).find('title').text
        except AttributeError:
            break
        links_list.append(url_dict)
    return links_list

def parse_to_json(chat_str):
    results = {}
    chat_mentions = parse_mentions(chat_str)
    if chat_mentions:
        results["mentions"] = chat_mentions

    chat_emoticons = parse_emoticons(chat_str)
    if chat_emoticons:
        results["emoticons"] = chat_emoticons
 
    chat_urls = parse_urls(chat_str)
    if chat_urls:
        results["links"] = chat_urls

    return json.dumps(results)