# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:56:32 2020

@author: lwwil
"""

import csv
import os
import re



# List all files in a directory using os.listdir
basepath = 'C:\\Users\\lwwil\\OneDrive\\Documents\\Python Scripts\\Game Scrapper\\gamescraper'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)