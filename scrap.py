import urllib2
from bs4 import BeautifulSoup
import xlwt

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
            if tournament.find(u'\xfa') != -1:
                tournament = tournament.replace(u'\xfa',"u")
            if tournament.find(u'\xb4') != -1:
                tournament = tournament.replace(u'\xb4', "And")
            if tournament.find(u'\u2019' ) != -1:
                tournament = tournament.replace(u'\u2019' , "'")
            if tournament.find(u'\xf4' ) != -1:
                tournament = tournament.replace(u'\xf4' , "o")
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

def get_statist_match(url,torneo, fecha_torneo):
    player1 = []
    player2 = []
    response = urllib2.urlopen(url)
    bs = BeautifulSoup(response, 'html.parser')
    names = bs.findAll('span', class_="first-name")
    last_names = bs.findAll('span', class_="last-name")
    if len(names)!=0:
        player1.append((transform_text(names[0].text).strip())+" "+transform_text(last_names[0].text).strip())
        player2.append(transform_text(names[1].text).strip()+" "+transform_text(last_names[1].text).strip())
        staticts1 = bs.findAll('td', class_ = 'match-stats-number-left')
        staticts2 = bs.findAll('td', class_='match-stats-number-right')
        for element1, element2 in zip(staticts1, staticts2):
            aux1 = transform_text(element1.text).strip()
            aux2 = transform_text(element2.text).strip()
            if aux1.find("%") != -1:
                aux1 = aux1.split("%")[0]
                aux2 = aux2.split("%")[0]
            player1.append(aux1)
            player2.append(aux2)
        winner = bs.findAll('td', class_= 'won-game')
        name = transform_text(winner[0].text).split(".")[1].strip()
        if last_names[0].text.find(name)!=-1:
            winner = transform_text(names[0].text).strip()+" "+transform_text(last_names[0].text).strip()
        else:
            winner = transform_text(names[1].text).strip()+" "+transform_text(last_names[1].text).strip()
    #falta sacar el ganador
    return [player1, player2, winner, torneo,fecha_torneo]

def write_xls(data):
    book = xlwt.Workbook(encoding="utf-8")
    sh = book.add_sheet("Sheet 1")
    for i in range(len(data)+1):
        if i == 0:
            sh.write(i, 0, "Player 1")
            sh.write(i, 1, "Player 2")
            sh.write(i, 2, "Serve Rating 1")
            sh.write(i, 3, "Serve Rating 2")
            sh.write(i, 4, "Aces 1")
            sh.write(i, 5, "Aces 2")
            sh.write(i, 6, "Double Faults 1")
            sh.write(i, 7, "Double Faults 2")
            sh.write(i, 8, "% 1st Serve 1")
            sh.write(i, 9, "% 1st Serve 2")
            sh.write(i, 10, "% 1st serve won 1")
            sh.write(i, 11, "% 1st serve won 2")
            sh.write(i, 12, "% 2nd serve won 1")
            sh.write(i, 13, "% 2nd serve won 2")
            sh.write(i, 14, "% Break point saved 1")
            sh.write(i, 15, "% Break point saved 2")
            sh.write(i, 16, "Served games played 1")
            sh.write(i, 17, "Served games played 2")
            sh.write(i, 18, "Return rating 1")
            sh.write(i, 19, "Return rating 2")
            sh.write(i, 20, "% 1st serve return won 1")
            sh.write(i, 21, "% 1st serve return won 2")
            sh.write(i, 22, "% 2nd serve return won 1")
            sh.write(i, 23, "% 2nd serve return won 2")
            sh.write(i, 24, "% Break point converted 1")
            sh.write(i, 25, "% Break point converted 2")
            sh.write(i, 26, "Return games played 1")
            sh.write(i, 27, "Return games played 2")
            sh.write(i, 28, "% Served point won 1")
            sh.write(i, 29, "% Served point won 2")
            sh.write(i, 30, "% Return point won 1")
            sh.write(i, 31, "% Return point won 2")
            sh.write(i, 32, "% Total point won 1")
            sh.write(i, 33, "% Total point won 2")
            sh.write(i, 34, "Winner")
            sh.write(i, 35, "Tournament")
            sh.write(i, 36, "Started date")
            sh.write(i, 37, "Ended date")
        else:
            for j in range(len(data[i-1][0])):
                if i != 0:
                    sh.write(i, 2*j, data[i-1][0][j])
                    sh.write(i, 2*j+1, data[i-1][1][j])
            sh.write(i, 2*len(data[i-1][0]), data[i-1][2])
            sh.write(i, 2*len(data[i-1][0])+1, data[i-1][3])
            sh.write(i, 2*len(data[i-1][0])+2, data[i-1][4][0])
            sh.write(i, 2*len(data[i-1][0])+3, data[i-1][4][1])
    book.save("ATPdata.xls")
    print "Save it!"