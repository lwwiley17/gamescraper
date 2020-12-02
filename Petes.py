# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:10:00 2020

@author: lwwil
"""

import csv
import re
from itertools import zip_longest

def main():
    #Team A is the perspective you want to view the game from
    teamA = input("Who is team A? ")
    if(teamA == "-1"):
        teamA = "(N.Y.)"
    #abvA is the shorthand side of field indicator
    abvA = input("What is shorthand for team A? ")
    if(abvA == "-1"):
        teamA = "MARITIME"
    get_games()
    breakdown(select_games(), teamA, abvA)

schedule = [
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
    '11. Football vs Salisbury University on 11.23.2019 - Box Score - Maritime College Athletics.csv',
    'Football vs Baylor on 11.23.2019 - Box Score - University of Texas Athletics.csv']




def get_games():
    for gm in schedule:
        print(gm)

def select_games():
    while True:
        try:
            val = int(input("What game do you want to break down? "))
            if (val > 0 and val <= len(schedule)):
                break
            print("Invalid game entered")
        except Exception as e:
            print(e)
    return val

#deciding the ODK based on the kick game and '*team* at mm:ss' cells
def getODK(cell, prevODK, teamA):
    runningODK = prevODK
    poss = re.findall(r".* at [0-9][0-9]:[0-9][0-9]", cell, re.IGNORECASE)
    if("kick" in cell or "punt" in cell):
        runningODK = "K"
    if(len(poss) > 0):
        #NEED TO PUT A DYNAMIC VARIABLE HERE
        #check = re.findall(r"\(N\.Y\.\)", poss[0], re.IGNORECASE)
        ball =  re.escape(teamA)
        check = re.findall(ball, poss[0], re.IGNORECASE)
        #NEED TO PUT A DYNAMIC VARIABLE HERE
        if(len(check) > 0):
            runningODK = "O"
        else:
            runningODK = "D"
    return runningODK

def getDN(cell):
    runningDN = "-1"
    down = re.findall(r"[0-9][a-z]+ and ([0-9]+|[GOAL]+)+ at [A-z]*[0-9]+", cell, re.IGNORECASE)
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
            runningDN = "Black Magic"
    else:
        runningDN = "No Info"
    return runningDN

def getDIST(cell):
    runningDIST = "-1"
    dist = re.findall(r"[0-9][a-z]+ and ([0-9]+|[GOAL]+) at [A-z]*([0-9]+)", cell, re.IGNORECASE)
    if(len(dist) > 0):
        if("GOAL" in dist[0]):
            runningDIST = dist[0][1]
        else:
            runningDIST = dist[0][0]
    else:
        runningDIST = "No Info"
    return runningDIST

def getYDLN(cell, poss, abvA):
    runningYDLN = "00"
    ydln = re.findall(r"[0-9][a-z]+ and ([0-9]+|[GOAL]+) at ([A-z]*)([0-9]+)", cell, re.IGNORECASE)
    if(len(ydln) > 0):
        if(ydln[0][2] == "50"):
            runningYDLN = ydln[0][2]
        #NEED TO PUT A DYNAMIC VARIABLE HERE
        elif(poss == "O" and abvA.lower() in ydln[0][1].lower()):
            runningYDLN = "-" + ydln[0][2]
        #NEED TO PUT A DYNAMIC VARIABLE HERE
        elif(poss == "O" and abvA.lower() not in ydln[0][1].lower()):
            runningYDLN = ydln[0][2]
        #NEED TO PUT A DYNAMIC VARIABLE HERE
        elif(poss == "D" and abvA.lower() in ydln[0][1].lower()):
            runningYDLN = ydln[0][2]
        #NEED TO PUT A DYNAMIC VARIABLE HERE
        elif(poss == "D" and abvA.lower() not in ydln[0][1].lower()):
            runningYDLN = "-" + ydln[0][2]
        else:
            print(cell)
            if("kickoff" in cell):
                runningYDLN = "-35"
            else:
                runningYDLN = "HELP"
            print(poss)
            print(ydln)
    else:
        runningYDLN = "No Info"
    return runningYDLN
                        
def getPLAYTYPE(cell):
    runningPLAYTYPE = "X"
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
    return runningPLAYTYPE

def getGNLS(cell):
    runningGNLS = "0"
    gain = re.findall("for ([0-9]+) yard", cell, re.IGNORECASE)
    loss = re.findall("for loss of ([0-9]) yard", cell, re.IGNORECASE)
    if(len(gain) > 0):
        runningGNLS = gain[0]
    elif(len(loss) > 0):
        runningGNLS = "-" + loss[0]
    elif("no gain" in cell or "incomplete" in cell or "interception" in cell):
        runningGNLS = "0"
    else:
        runningGNLS = "No Info"
    return runningGNLS

def getRESULT(cell):
    runningRESULT = "X"
    if("touchdown" in cell or "TOUCHDOWN" in cell):
        if("blocked" in cell):
            runningRESULT = "Blocked, Def TD"
        elif("complete" in cell):
            runningRESULT = "Complete, TD"
        elif("fumble" in cell):
            runningRESULT = "Fumble, Def TD"
        elif("no good" in cell):
            runningRESULT = "No Good, Def TD"
        elif("interception" in cell):
            runningRESULT = "Interception, Def TD"
        elif("rush" in cell):
            runningRESULT = "Rush, TD"
        elif("scramble" in cell):
            runningRESULT = "Scramble, TD"
        else:
            runningRESULT = "TD"
    elif("safety" in cell):
        if("penalty" in cell):
            runningRESULT = "Penalty, Safety"
        elif("rush" in cell):
            runningRESULT = "Rush, Safety"
        elif("sack" in cell):
            runningRESULT = "Sack, Safety"
        else:
            runningRESULT = "Safety"
    elif("fumble" in cell):
        if("complete" in cell):
            runningRESULT = "Complete, Fumble"
        elif("interception" in cell):
            runningRESULT = "Interception, Fumble"
        elif("sack" in cell):
            runningRESULT = "Sack, Fumble"
        else:
            runningRESULT = "Fumble"
    elif("block" in cell):
        runningRESULT = "Block"
    elif("incomplete" in cell):
        runningRESULT = "Incomplete"
    elif("complete" in cell):
        runningRESULT = "Complete"
    elif("downed" in cell):
        runningRESULT = "Downed"
    elif("fair catch" in cell):
        runningRESULT = "Fair Catch"
    elif("No Good" in cell):
        runningRESULT = "No Good"
    elif("good" in cell or "GOOD" in cell):
        runningRESULT = "Good"
    elif("out of bounds" in cell):
        runningRESULT = "Out of Bounds"
    elif("return" in cell):
        runningRESULT = "Return"
    elif("rush" in cell):
        runningRESULT = "Rush"
    elif("sack" in cell):
        runningRESULT = "Sack"
    elif("scramble" in cell):
        runningRESULT = "Scramble"
    elif("timeout" in cell or "Timeout" in cell):
        runningRESULT = "Timeout"
    elif("touchback" in cell):
        runningRESULT = "Touchback" 
    elif("penalty" in cell or "PENALTY" in cell):
        runningRESULT = "Penalty"
    else:
        runningRESULT = "No Info" 
    
    return runningRESULT
    
def breakdown(gm, teamA, abvA):
    game = schedule[gm-1]

    #Getting Team that is playing
    opp = re.findall('vs (.+) on', game, re.IGNORECASE)
    if opp:
        opponent  = opp[0].strip()
        print(opponent )
    #Getting date of game
    d = re.findall('[0-9][0-9]?\.[0-9][0-9]?\.[0-9][0-9][0-9][0-9]', game, re.IGNORECASE)
    if d:
        date = d[0].strip()
        print(date)
    
    #Organizing dates mm.dd.yyyy
    if date[2] != '.':
        date = "0" + date
        print(date)
    
    #Reading raw play-by-play data
    with open(f'{game}','r') as f:
        csv_reader = csv.reader(f)
        
        #Writing into Hudl ready file
        with open(f'{date} {opponent}.csv','w') as g:        
            thewriter = csv.writer(g, delimiter = ',', lineterminator = '\n')
            
            #desired columns for hudl breakdown
            playlist = { 
                'PLAY #' : [],
                'ODK' : [],
                'DN' : [],
                'DIST' : [],
                'YARD LN' : [],
                'PLAY TYPE' : [],
                'GN/LS' : [],
                'RESULT' : []
                }
            
            #print(csv_reader)
            playcount = 0
            column = 0

            
            #going full play by play of the game
            for line in csv_reader:
                
                ### PLAY # ###
                playcount = playcount + 1
                playlist.get("PLAY #").append(playcount)
                
                for cell in line:
                    
                    ### PLAY # ###
                    # taken care of in the exterior loop
                    
                    if(column == 0):
                        
                        ### ODK ###  
                        if(len(playlist.get("ODK")) > 0):
                            prevODK = playlist.get("ODK")[-1]
                        else:
                            prevODK = "X"
                        playlist.get("ODK").append(getODK(cell,prevODK, teamA))
                        
                        ### DN # ###
                        playlist.get("DN").append(getDN(cell))
                        
                        ### DIST # ###
                        playlist.get("DIST").append(getDIST(cell))

                        ### YDLN # ###
                        playlist.get("YARD LN").append(getYDLN(cell, playlist.get("ODK")[-1],abvA))
                        
                        #need this to balance out rows with only 1 cell, fill in "2nd half" of data
                        #primarily issues occur with kickoff to start half and pre/post game inputs
                        if(line[0] == line[-1] and "kickoff" in cell):
                            playlist.get("YARD LN")[-1] = "-35"
                            playlist.get("PLAY TYPE").append("KO")
                            playlist.get("GN/LS").append("No Info")
                            playlist.get("RESULT").append("Need to make things methods")
                        elif(line[0] == line[-1]):
                            playlist.get("PLAY TYPE").append("---")
                            playlist.get("GN/LS").append("---")
                            playlist.get("RESULT").append("---")
                        
                        
                    elif(column == 1):
                        ### PLAYTYPE ###
                        playlist.get("PLAY TYPE").append(getPLAYTYPE(cell))
                        
                        #this info comes from right hand column, couldn't figure out easier way
                        if(getPLAYTYPE(cell) in ["KO", "PUNT", "FG", "Extra Pt."]):
                            playlist.get("ODK")[-1] = "K"
                            
                        ### GNLS # ###
                        playlist.get("GN/LS").append(getGNLS(cell))
                        
                        ### RESULT ###
                        playlist.get("RESULT").append(getRESULT(cell))
                        
                    column = column + 1
                column = 0
            
            ###
            ### BLACK MAGIC IDK HOW IT WORKS
            ###
            
            zd = list(zip_longest(*playlist.values()))
            thewriter.writerow(playlist.keys())
            for items in zd:
                  thewriter.writerow(items)

if __name__ == "__main__":
    main()