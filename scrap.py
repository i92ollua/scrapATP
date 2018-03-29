import urllib2
from bs4 import BeautifulSoup
import re

def download_html(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def lookfor_html(html,element):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.findAll(element)

def get_first_part(labels):
    urls = []
    for td in labels:
        iteration = td.next_element.next_element
        if iteration.name == 'a' and iteration['href'].find("en/scores/archive/"):
            urls.append(str(iteration['href']))
    return urls

def get_tournaments(labels):
    tournaments = []
    for td in labels:
        iteration = td.next_element.next_element
        if iteration.name == 'span':
            tournament =iteration.text
            if tournament.find(u"\u00E5") != -1:
                tournament = tournament.replace(u"\u00E5","a")
            tournament = transform_text(tournament)
            tournaments.append(str(tournament))
    return tournaments

def get_date_tournament(html):
    start = ""
    end = ""
    bs = BeautifulSoup(html, 'html.parser')
    searching = bs.findAll('span', class_ = "tourney-dates")
    if searching.__len__() != 0:
        aux = str(searching[0].text)
        aux = transform_text(aux)
        aux = aux.replace(" - ",".")
        aux = aux.split(".")
        start = aux[2]+"/"+aux[1]+"/"+aux[0]
        end = aux[5]+"/"+aux[4]+"/"+aux[3]
    date = [start,end]
    return date

def transform_text(text):
    text_transformed = text.replace("\t", "")
    text_transformed = text_transformed.replace("\r", "")
    text_transformed = text_transformed.replace("\n", "")
    return text_transformed

def get_url_matches(html):
    urls = []
    bs = BeautifulSoup(html, 'html.parser')
    searching = bs.findAll('a', class_=" ")
    for element in searching:
        urls.append(str(element['href']))
    return urls

def get_statist_match(url):
    player1 =[]
    player2 =[]
    response = urllib2.urlopen(url)
    bs = BeautifulSoup(response, 'html.parser')
    names = bs.findAll('span', class_="first-name")
    last_names = bs.findAll('span', class_="last-name")
    player1.append((transform_text(names[0].text).strip()))
    player1.append(transform_text(last_names[0].text).strip())
    player2.append(transform_text(names[1].text).strip())
    player2.append(transform_text(last_names[1].text).strip())
    staticts1= bs.findAll('td', class_ = 'match-stats-number-left')
    staticts2 = bs.findAll('td', class_='match-stats-number-right')
    for element1,element2 in zip(staticts1,staticts2):
        aux1 = transform_text(element1.text).strip()
        aux2 = transform_text(element2.text).strip()
        player1.append()
        player2.append()
    return [player1,player2]