# Steemnova_stats
Daily statistics for SteemNova game - https://steemnova.intinte.org/.

Results you can see here https://steemit.com/@sentipl

## Description
Scripts to import and analyze statistics of users of SteemNova game. It can be uses to any game based on Classic OGame engine.

## Technologies
* Python 3.7
* MySQL database
* mysql.connector library

## Setup
First create database and enter loging details into local_config dictionary in file databases.py. To create database use commends from create_databse.txt file.
You also need access to Ogame database (at least SELECTS). Login details enter into config dicitonary in databases.py.
Execute import.py and generator.py afterwards. The post to post on steemit.com is generated to file result.txt.

## Credits
Created by MarekPas
