# Steemnova_stats
Daily statistics for SteemNova game - https://steemnova.intinte.org/
Results you can see here https://steemit.com/@sentipl

## Description
Scripts to import and alayze statistics of users who play SteemNova game. Game is based on OGame.

## Technologies
* Python 3.7
* MySQL database
* mysql.connector library

## Setup
First create database and enter loging details into local_config dictionary in files import.py and generator.py.
You also need SELECT access to Ogame database. This login details enter into config dicitonary in files import.py and generator.py.
Start import.py then start generator.py. You will see statistics in command prompt. Post to post on steemit.com is generated to file result.txt.

## Credits
Created by MarekPas
