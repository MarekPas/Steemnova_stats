import mysql.connector
import time
from databases import config, local_config
from datetime import date, timedelta

table = "sn1_users"

def importer(table, indexer="max"):
    mycursor = sql.cursor(buffered=True)
    mycursor.execute(f"DELETE FROM {table} WHERE `{today}` is null")
    sql.commit()
    if indexer == "min":
        mycursor.execute(f"SELECT sn1_users.name, {table}.`{today}` - {table}.`{yesterday}` AS result FROM sn1_users JOIN {table} ON sn1_users.id = {table}.id ORDER BY COALESCE(result, 0) ASC LIMIT 1")
        result = mycursor.fetchone()
    elif indexer == "max":
        mycursor.execute(f"SELECT sn1_users.name, {table}.`{today}` - {table}.`{yesterday}` AS result FROM sn1_users JOIN {table} ON sn1_users.id = {table}.id ORDER BY COALESCE(result, 0) DESC LIMIT 1")
        result = mycursor.fetchone()
    return result[0].strip(), result[1]

def string_with_at(ls, newline=False):  #adding "@" to players who has no " " in nickname
    result = ""
    if newline:
        for name in ls:
            if " " in name:
                result += " " + name[0].strip() + "\n"
            else:
                result += " @" + name[0].strip() + "\n"
    else:
        for name in ls:
            if " " in name:
                result += " " + name[0].strip() + ","
            else:
                result += " @" + name[0].strip() + ","
    return result

def new_users():
    mycursor.execute(f"SELECT `name` FROM sn1_users WHERE `{yesterday}` is NULL")
    new_ = ()
    for i in mycursor.fetchall():
        new_ += i
    new_players = string_with_at(new_, newline=True)
    if new_players == "":
        new_players = "No new players today"
        print("No new players today\n")
    else:
        print("New players:\n", new_players)
    return new_players

def deleted_players():
    delcursor = sql.cursor()
    delcursor.execute(f"SELECT name FROM {table} WHERE `{today}` IS Null")
    d = delcursor.fetchall()
    deleted = string_with_at(d, newline=True)
    if deleted == "":
        deleted = "Noone left us today"
        print("Noone left us today\n")
    else:
        print("Deleted players:\n", deleted)
        with open("E:/steemnova/deleted.txt", "a") as fd:
            fd.write(f"{today}\n{deleted}")
    delcursor.execute(f"DELETE FROM {table} WHERE `{today}` IS Null")
    sql.commit()
    return deleted

def check_last_previous_day():
    succes = False
    day = 1
    while succes == False:
        try:
            yesterday = str(date.today() - timedelta(days=day))
            cursor = sql.cursor(buffered=True)
            cursor.execute(f"SELECT `{yesterday}` FROM sn1_users")
            succes = True
        except:
            day += 1
            continue
    print(f"Last update was {day} day(s) ago.")
    return yesterday

def warning_players():
    time_ms = int(time.time())
    days_ms = time_ms - 7689600    # 89 days
    sql = mysql.connector.connect(**config)
    mycursor = sql.cursor(buffered=True)
    mycursor.execute(f"select username from uni1_users where onlinetime <={days_ms}")
    result = mycursor.fetchall()
    sql.close()
    warned = ""
    if len(result) > 0:
        warned = string_with_at(result)
        warned = warned.strip(",")
        warned = warned.lstrip(" ")
        warned += " you may be deleted soon due to inactivity. Maybe it's time to come back to the game? :)"
    print("Warning: ", warned)
    return warned

def vacations():
    sql = mysql.connector.connect(**config)
    vac_cursor = sql.cursor()
    vac_cursor.execute("select count(*) from uni1_users where urlaubs_modus=1")
    holidays = vac_cursor.fetchone()[0]
    vac_cursor.execute("select count(*) from uni1_users")
    users = vac_cursor.fetchone()[0]
    print("Players:", users, "On vacation:", holidays)
    sql.close()
    return users, holidays

sql = mysql.connector.connect(**local_config)
mycursor = sql.cursor(buffered=True)

today = str(date.today())
yesterday = check_last_previous_day()

# Top 3 earners
mycursor.execute(f"SELECT name, `{today}` - `{yesterday}` AS result FROM {table} order by result DESC limit 3")
top = mycursor.fetchall()
print(top[0][0], top[1][0], top[2][0])

# Top 3 losers
mycursor.execute(f"SELECT name, `{today}` - `{yesterday}` AS result FROM {table} WHERE `{yesterday}` IS NOT NULL order by COALESCE(result, 0) ASC LIMIT 3")
bottom = mycursor.fetchall()
print(bottom[0][0], bottom[1][0], bottom[2][0])

mycursor.execute(f"SELECT AVG(`{today}`) FROM sn1_users ")
average = int(mycursor.fetchone()[0])
print("Average:", average)

new_players = new_users()
deleted_players = deleted_players()

# DESTROYER
destroyer_name, destroyer_score = importer("sn1_destroyer", "max")
destroyer_score = int(destroyer_score / 1000)
print("Destroyer:", destroyer_name, destroyer_score)

# FLEET BUILDER
builder_name, builder_score = importer("sn1_fail", "max")
print("Fleet Builder:", builder_name, builder_score)

# BUNKER
bunker_name, bunker_score = importer("sn1_bunker", "max")
print("Bunkerman:", bunker_name, bunker_score)

# AGRESOR
agresor_name, agresor_score = importer("sn1_agresor", "max")
print("Agresor:", agresor_name, agresor_score)

# FARM
farma_name, farma_score = importer("sn1_farm", "max")
print("Farma:", farma_name, farma_score)

# FAIL
fail_name, fail_score = importer("sn1_fail", "min")
print("Fail of the day:", fail_name, fail_score)

sql.close()

users, holidays = vacations()
warned = warning_players()

day = time.strftime('%d.%m.%Y')

with open("E:/steemnova/result.txt", "w") as plik:
    plik.write(f"""
<center><p>SteemNova - Daily statistics and achievements {day}</p>
https://static.xx.fbcdn.net/images/emoji.php/v9/tbd/1/28/1f4f6.png Daily statistics for <a href="https://steemnova.intinte.org/"><b>SteemNova</b></a> https://static.xx.fbcdn.net/images/emoji.php/v9/tbd/1/28/1f4f6.png</b>
  
</br>
<b>Players:</b> {users}
On vacation: {holidays}
Average points: {average}</br>
<b>New players:</b>
{new_players}
<b>Deleted players:</b>
{deleted_players}</br>

<b>Top earners of the day:</b>
Position | Player | Points
- | ------------ | -------------
1.|@{top[0][0]}|+{top[0][1]}
2.|@{top[1][0]}|+{top[1][1]}
3.|@{top[2][0]}|+{top[2][1]}

<b>Top losers of the day:</b>
Position | Player | Points
- | ------------ | -------------
1.|@{bottom[0][0]}|{bottom[0][1]}
2.|@{bottom[1][0]}|{bottom[1][1]}
3.|@{bottom[2][0]}|{bottom[2][1]}
</br>
<center><h2>https://static.xx.fbcdn.net/images/emoji.php/v9/t9f/1/28/1f3c6.png Achievements https://static.xx.fbcdn.net/images/emoji.php/v9/t9f/1/28/1f3c6.png </h2></center>


Destroyer of the day | Player | Destroyed Fleet Points
-- | ------------ | ------------ 
https://media.tenor.co/images/89ba44847971c53223704fe9323caacb/tenor.gif |@{destroyer_name}| <center>{destroyer_score}</center>

Fleet Builder of the day | Player | Fleet points
-- | ------------ | ------------ 
https://media.tenor.co/images/f4fe55de834960c603f09e1fea6a156d/tenor.gif |@{builder_name}|<center>+{builder_score}</center>

Bunkerman of the day | Player | Defense Points
-- | ------------ | ------------ 
https://media.tenor.co/images/940e525e4033fedc6910515f386d3902/tenor.gif |@{bunker_name}| <center>+{bunker_score}</center>

Agressor of the day | Player | Battles won
-- | ------------ | ------------ 
https://media.tenor.co/images/f7b498a905f3e8c964ad5d97bf176e1f/tenor.gif |@{agresor_name}|<center>{agresor_score}</center>

Farm of the day | Player | Battles lost
-- | ------------ | ------------ 
https://media.tenor.co/images/6a28bad348a6d006ddfb25aea8c166da/tenor.gif |@{farma_name}| <center>{farma_score}</center>

Epic fail of the day | Player | Fleet Points
-- | ------------ | ------------ 
https://media.tenor.co/images/0cc3ca22b2720ecc97d6f9ce6fd357bc/tenor.gif |@{fail_name}| <center>{fail_score}</center>

{warned}
</center>
<center>https://steemnova.intinte.org/</center>
https://steemnova.intinte.org/styles/resource/images/meta.png
""")
