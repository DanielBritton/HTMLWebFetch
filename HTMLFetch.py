import re
from bs4 import BeautifulSoup
import requests
import os
import shutil


def get_html(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, features='lxml')
    return html


def getLinks(data):
    links = []
    for link in data.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
    return links


def removeDuplicates(links):
    unique = []
    for i in links:
        if i not in unique:
            unique.append(i)
    return unique


url = input('FORMAT:  http://www.url.com \nDEFAULT URL:  http://www.python.org \nWhat URL would you like to load? (To use default URL, press enter) ')
if len(url) < 12:
    url = "http://www.python.org"

print('Loading', url)
data = get_html(url)

print('Finding Child Links')
links = getLinks(data)

if len(links) == 0:
    print('No Child Links')
else:
    links = removeDuplicates(links)
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('output')

    print('Importing HTML Files')
    for index, value in enumerate(links):
        HTML = get_html(value).prettify()
        fileName = "output/output"+str(index+1)
        print('Creating', fileName)
        with open(fileName+'URL.txt', "w", encoding='utf-8') as file:
            file.write(value)
        with open(fileName+'.html', "w", encoding='utf-8') as file:
            file.write(HTML)

    print('Done - Files available at /output')
