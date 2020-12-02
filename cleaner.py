# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:56:32 2020

@author: lwwil
"""

import csv
import os
import re

def main():
    cleangame(selectgame())
    
def selectgame():
    i = 1
    for item in os.listdir():
        print(str(i) + " " + item)
        i += 1
        
    while True:
        try:
            val = int(input("What game do you want to break down? "))
            if (val > 0 and val <= len(os.listdir())):
                break
            print("Invalid game entered, enter the number next to the game")
        except Exception as e:
            print(e)
    dirty = os.listdir()[val-1]
    
    return dirty

def cleangame(gm):
    count = 1
    with open(f'{gm}', 'r') as inp, open(f'cleaned {gm}', 'w') as out:
        writer = csv.writer(out, delimiter = ',', lineterminator = '\n')
        for row in csv.reader(inp):
            if "HELP" in row:
                row[4] = -35
            if row[1] != "X":
                if row[7] != "---":
                    if str(row[2]).lower() != "no info" or str(row[3]).lower() != "no info" or str(row[4]).lower() != "no info":
                        if str(row[5]).lower() != "no info" or str(row[6]).lower() != "no info" or str(row[7]).lower() != "no info":
                            if "Need to make things methods" in row:
                                row[7] = ""
                            if "No Info" in row or "No info" in row:
                                for i in range(len(row)):
                                    if "No Info" == row[i] or "No info" == row[i]:
                                        row[i] = ""
                            row[0] = count
                            writer.writerow(row)
                            count += 1
                        else:
                            print("4th" + str(row))
                    else:
                        print("3rd" + str(row))
                else:
                    print("2nd" + str(row))
            else:
                print("1st" + str(row))
        
if __name__ == "__main__":
    main()