from bs4 import BeautifulSoup
import requests
import csv

#Use this line for individual games
source = requests.get("https://maritimeathletics.com/sports/football/stats/2019/salisbury-university/boxscore/7035").text

#Use this line for entire seasons
#TO BE COMPLETED

soup = BeautifulSoup(source, 'lxml')

name = soup.find("title").text.strip()
name = name.replace('/','.')
game = soup.find(id="play-by-play")

with open(f"{name}.csv", "w", newline="") as f:
    thewriter = csv.writer(f)
    count = 0
    for table in game.find_all('table'):
        for row in table.find_all('tr'):
            temp = []
            for data in row.find_all('td'):
                temp.append(data.text.strip())
            if len(temp) > 0:
                thewriter.writerow(temp)