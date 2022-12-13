from bs4 import BeautifulSoup
import requests
import csv

url = 'https://en.wikipedia.org/wiki/FIFA_World_Cup'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

#Get Links for World Cups in Overview Table
attendance = soup.find('h2', string='Attendance')
overviewTable = attendance.find_next('table')
links = overviewTable.find_all('a')
worldCups = []
for link in links:
    href = link['href']
    if (href.endswith('FIFA_World_Cup')):
        url = 'https://en.wikipedia.org' + href
        worldCups.append(url)

# SPECIAL LOGIC 1978/1982/1986/1990/1994/1998/2006 GROUP STAGE

worldCupCount = 0
for worldCup in worldCups:
    print(worldCupCount)
    page = requests.get(worldCup)
    soup = BeautifulSoup(page.text, 'html.parser')

    #Crawl one game logic
    year = soup.find('h1', id='firstHeading').get_text()[0:4]

    games = soup.find_all('div', class_='footballbox')
    iteration = 0
    for game in games:
        teamA = game.find('th', class_='fhome').get_text().strip()
        teamB = game.find('th', class_='faway').get_text().strip()
        score = game.find('th', class_='fscore').get_text()
        print(teamA + ' ' + teamB + ' ' + score)
        overtime = False
        if 'a.e.t' in score:
            overtime = True
            score = score.split(' ')[0]
        if '–' in score:
            goalsA = score.split('–')[0]
            goalsB = score.split('–')[1]
            if (int(goalsA) > int(goalsB)):
                winner = 'teamA'
            elif (int(goalsA) == int(goalsB)):
                winner = 'draw'
                if overtime:
                    winner = 'unclear'
            elif (int(goalsA) < int(goalsB)):
                winner = 'teamB'
            else:
                winner = 'ERROR'
        else:
            goalsA = 'unclear'
            goalsB = 'unclear'

        #WRITE TO CSV
        with open('WorldCupData.csv', mode='a', newline='', encoding='utf-8') as outputFile:
            worldCupCSV = csv.writer(outputFile, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)

            if (worldCupCount == 0 and iteration == 0):
                worldCupCSV.writerow(['year', 'teamA', 'teamB', 'goalsA', 
                    'goalsB', 'winner'])
        
            worldCupCSV.writerow([year, teamA, teamB, goalsA, goalsB, winner])
        iteration = iteration + 1
    worldCupCount = worldCupCount+1
