# Steemnova_stats
Daily statistics for SteemNova game - https://steemnova.intinte.org/.

You can check results on:
* https://ecency.com/@sentipl
* https://peakd.com/@sentipl
* https://steemit.com/@sentipl (not updating anymore).

## Description
Scripts to import and analyze statistics of SteemNova players. It's a game based on Classic OGame engine.

## Technologies
* Python 3.7
* MySQL database
* mysql.connector library

## Setup
You need access to Ogame database (at least SELECTS). Login details enter into config dicitonary in databases.py.
Create local database and enter login details into local_config dictionary in databases.py. To create database use commands from create_databse.txt file.
Execute import.py and generator.py afterwards. The post is generated to result.txt file.

## Credits
Created by MarekPas
