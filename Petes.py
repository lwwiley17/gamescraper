# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:10:00 2020

@author: lwwil
"""

import csv
import os
import re
from itertools import zip_longest

#print(os.listdir())
"""
'01. Football vs Maine Maritime on 9.7.2019 - Box Score - Maritime College Athletics.csv', 
'02. Football vs Mass. Maritime on 9.13.2019 - Box Score - Maritime College Athletics.csv', 
'03. Football vs Merchant Marine on 9.21.2019 - Box Score - Maritime College Athletics.csv', 
'04. Football vs William Paterson on 9.28.2019 - Box Score - Maritime College Athletics.csv', 
'05. Football vs Dean on 10.12.2019 - Box Score - Maritime College Athletics.csv', 
'06. Football vs Castleton on 10.19.2019 - Box Score - Maritime College Athletics.csv', 
'07. Football vs Anna Maria on 10.26.2019 - Box Score - Maritime College Athletics.csv', 
'08. Football vs Gallaudet on 11.2.2019 - Box Score - Maritime College Athletics.csv', 
'09. Football vs Alfred State on 11.9.2019 - Box Score - Maritime College Athletics.csv', 
'10. Football vs Mount St. Joseph on 11.16.2019 - Box Score - Maritime College Athletics.csv', 
'11. Football vs Salisbury University on 11.23.2019 - Box Score - Maritime College Athletics.csv'
"""

game = '01. Football vs Maine Maritime on 9.7.2019 - Box Score - Maritime College Athletics.csv'

#Getting Team that is playing
opp = re.search('vs(.+?)on', game)
if opp:
    opponent  = opp.group(1).strip()
    print(opponent )
    
#Getting date of game
d = re.search('on(.+?)-', game)
if d:
    date = d.group(1).strip()
    print(date)

#Organizing dates
if date[2] != '.':
    date = "0" + date
    print(date)

with open(f'{game}','r') as f:
    csv_reader = csv.reader(f)
    
    with open(f'{date} {opponent}.csv','w') as g:
        fieldnames = ['PLAY #', 'ODK', 'DN', 'DIST', 'YDLN', 'PLAYTYPE', 'GNLS', 'RESULT']
        
        thewriter = csv.writer(g, delimiter = ',', lineterminator = '\n')
        
        #THIS IS WHERE I NEED REGEX MAGIC
        playlist = { 
            'PLAY #' : [],
            'ODK' : [],
            'DN' : [],
            'DIST' : [],
            'YDLN' : [],
            'PLAYTYPE' : [],
            'GNLS' : [],
            'RESULT' : []
            }
        
        #print(csv_reader)
        playcount = 0
        column = 0
        runningODK = "X"
        runningDN = "-1"
        runningDIST = "-1"
        runningYDLN = "00"
        runningPLAYTYPE = "X"
        for line in csv_reader:
            playcount = playcount + 1
            playlist.get("PLAY #").append(playcount)
            for cell in line:
                
                #if (column == 0):
                    
                ### PLAY # ###
                # taken care of in the exterior loop
                
                ### ODK ###      
                poss = re.findall(r".* at [0-9][0-9]:[0-9][0-9]", cell)
                if("kick" in cell or "punt" in cell):
                    runningODK = "K"
                if(len(poss) > 0):
                    check = re.findall(r"\(N\.Y\.\)", poss[0])
                    if("(N.Y.)" in check):
                        runningODK = "O"
                    else:
                        runningODK = "D"
                playlist.get("ODK").append(runningODK)
                
                ### DN # ###
                down = re.findall(r"[0-9][a-z]+ and ([0-9]+|[GOAL]+)+ at [A-z]*[0-9]+", cell)
                if(len(down) > 0 ):
                    if('1st' in cell):
                        runningDN = 1
                    elif('2nd' in cell):
                        runningDN = 2
                    elif('3rd' in cell):
                        runningDN = 3
                    elif('4th' in cell):
                        runningDN = 4
                    else:
                        runningDN = -22
                        print(down)
                else:
                    runningDN = -11
                playlist.get("DN").append(runningDN)
                
                ### DIST # ###
                dist = re.findall(r"[0-9][a-z]+ and ([0-9]+|[GOAL]+) at [A-z]*([0-9]+)", cell)
                if(len(dist) > 0):
                    if("GOAL" in dist[0]):
                        runningDIST = dist[0][1]
                    else:
                        runningDIST = dist[0][0]
                playlist.get("DIST").append(runningDIST)
                
                ### YDLN # ###
                ydln = re.findall(r"[0-9][a-z]+ and ([0-9]+|[GOAL]+) at ([A-z]*)([0-9]+)", cell)
                if(len(ydln) > 0):
                    if(runningODK == "O" and "MARITIME" in ydln[0][1]):
                        runningYDLN = "-" + ydln[0][2]
                    elif(runningODK == "O" and "MARITIME" not in ydln[0][1]):
                        runningYDLN = ydln[0][2]
                    elif(runningODK == "D" and "MARITIME" in ydln[0][1]):
                        runningYDLN = ydln[0][2]
                    elif(runningODK == "D" and "MARITIME" not in ydln[0][1]):
                        runningYDLN = "-" + ydln[0][2]
                    else:
                        runningYDLN = "FUCK"
                else:
                    runningYDLN = "No info"
                
                playlist.get("YDLN").append(runningYDLN)
                
                ### PLAYTYPE ###
                if("kickoff" in cell):
                    runningPLAYTYPE = "KO"
                elif("punt" in cell):
                    runningPLAYTYPE = "PUNT"
                elif("field goal" in cell):
                    runningPLAYTYPE = "FG"
                elif("kick attempt" in cell):
                    runningPLAYTYPE = "Extra Pt."
                elif("rush attempt" in cell or "pass attempt" in cell):
                    runningPLAYTYPE = "2 Pt."
                elif("rush" in cell):
                    runningPLAYTYPE = "Run"
                elif("pass" in cell):
                    runningPLAYTYPE = "Pass"
                else:
                    runningPLAYTYPE = "No Info"
                playlist.get("PLAYTYPE").append(runningPLAYTYPE)
                
                ### GNLS # ###
                
                playlist.get("GNLS").append("100")
                
                
                ### RESULT ###
                playlist.get("RESULT").append("BAD")
                
                column = column + 1 
            column = 0
        
        
        zd = list(zip_longest(*playlist.values()))
        thewriter.writerow(playlist.keys())
        for items in zd:
              thewriter.writerow(items)