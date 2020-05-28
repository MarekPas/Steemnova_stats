import mysql.connector
from databases import config, local_config
from datetime import date, timedelta

def importer(table, indexer="max"):
    sql = mysql.connector.connect(**local_config)
    mycursor = sql.cursor(buffered=True)
    mycursor2 = sql.cursor(buffered=True)
    mycursor.execute(f"SELECT id,`{today}` FROM {table} ORDER BY id")
    pointsa = mycursor.fetchall()
    player_score = 0
    player_id = None
    for a, b in pointsa:
        if b is None:
            mycursor.execute(f"DELETE FROM {table} WHERE id = \"{a}\"")
            sql.commit()
        else:
            mycursor2.execute(f"SELECT `{yesterday}` FROM {table} WHERE id=\"{a}\"")
            yp = mycursor2.fetchone()[0]
            if yp is None:
                continue
            x = b - yp
            if indexer == "min":
                if x < player_score:
                    player_score = x
                    player_id = a
            elif indexer == "max":
                if x > player_score:
                    player_score = x
                    player_id = a
    mycursor.execute(f"SELECT name FROM sn1_users WHERE id={player_id}")
    player_name = mycursor.fetchone()[0].rstrip()
    sql.close()
    return player_name, player_score

def deleted_players():
    sql = mysql.connector.connect(**local_config)
    delcursor = sql.cursor()
    delcursor.execute(f"SELECT name FROM {table} WHERE `{today}` IS Null")
    d = delcursor.fetchall()
    deleted = ""
    for name in d:
        deleted += "@" + name + "\n"    # formating deleted players into string (each player in new line)
    if deleted == "":
        deleted = "Noone left us today"
        print("Noone left us today")
    else:
        print("Deleted players:\n", deleted)
        with open("E:/steemnova/deleted.txt", "a") as fd:
            fd.write(f"{today}\n{deleted}")
    return deleted

def vacations():
    sql1 = mysql.connector.connect(**config)
    vac_cursor = sql1.cursor()
    vac_cursor.execute("select count(*) from uni1_users where urlaubs_modus=1")
    holidays = vac_cursor.fetchone()[0]
    vac_cursor.execute("select count(*) from uni1_users")
    users = vac_cursor.fetchone()[0]
    print("Players:", users, "On vacation:", holidays)
    sql1.close()
    return users, holidays

def new_users():
    mycursor.execute(f"SELECT `name` FROM sn1_users WHERE `{yesterday}` is NULL")
    new_ = ()
    for i in mycursor.fetchall():
        new_ += i
    new_players = ""
    for k in new_:
        new_players += "@" + k.rstrip() + "\n"  # formating new players into string (each player in new line)
    if new_players == "":
        new_players = "No new players today"
        print("No new players today\n")
    else:
        print("New players:\n", new_players)
    sql.close()
    return new_players

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
            print(day)
            continue
    return yesterday


sql = mysql.connector.connect(**local_config)
mycursor = sql.cursor(buffered=True)

today = str(date.today())
yesterday = check_last_previous_day()

table = "sn1_users"

# Top 3 earners
mycursor.execute(f"SELECT name, `{today}` - `{yesterday}` AS result FROM {table} order by result DESC limit 3")
top = mycursor.fetchall()
first, second, third = top[0][1], top[1][1], top[2][1]
one, two, three = top[0][0], top[1][0], top[2][0]
print(one, first, two, second, three, third)

# Top 3 losers
mycursor.execute(f"SELECT name, `{today}` - `{yesterday}` AS result FROM {table} WHERE `{yesterday}` IS NOT NULL order by result ASC LIMIT 3")
top = mycursor.fetchall()
firstx, secondx, thirdx = top[0][1], top[1][1], top[2][1]
onex, twox, threex = top[0][0], top[1][0], top[2][0]
print(onex, firstx, twox, secondx, threex, thirdx)

mycursor.execute(f"SELECT AVG(`{today}`) FROM sn1_users ")
average = int(mycursor.fetchone()[0])
print("Średnia:", average)

users, holidays = vacations()
new_players = new_users()
deleted_players = deleted_players()

class Player:
    def setName(self, value):
        self.name = value[0]
        self.score = value[1]

# DESTROYER (class)
destroyer = Player()
destroyer.setName(importer("sn1_destroyer", "max"))
destroyer.score = int(destroyer.score / 1000)
print("Destroyer:", destroyer.name, destroyer.score)

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

with open("E:/steemnova/result.txt", "w") as plik:
    plik.write(f"""
<p>SteemNova is a space-war strategy game based on classic OGame <a href="https://en.wikipedia.org/wiki/Massively_multiplayer_online_game">MMO</a> with hundreds of players who compete to each other trying to be the best in universe. Everything what you need to play is a standard browser. STEEM or HIVE account is not required but if you have it, you will be rewarded with STEEM and HIVE tokens just for playing the game. The better you are - the more tokens you get. Join today by clicking link below!</p>
<center>https://static.xx.fbcdn.net/images/emoji.php/v9/tbd/1/28/1f4f6.png Daily statistics for <a href="https://steemnova.intinte.org/"><b>SteemNova</b></a> https://static.xx.fbcdn.net/images/emoji.php/v9/tbd/1/28/1f4f6.png</b>
  
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
1.|@{one}|+{first}
2.|@{two}|+{second}
3.|@{three}|+{third}

<b>Top losers of the day:</b>
Position | Player | Points
- | ------------ | -------------
1.|@{onex}|{firstx}
2.|@{twox}|{secondx}
3.|@{threex}|{thirdx}
</br>
<center><h2>https://static.xx.fbcdn.net/images/emoji.php/v9/t9f/1/28/1f3c6.png Achievements https://static.xx.fbcdn.net/images/emoji.php/v9/t9f/1/28/1f3c6.png </h2></center>


Destroyer of the day | Player | Destroyed Fleet Points
-- | ------------ | ------------ 
https://media.tenor.co/images/89ba44847971c53223704fe9323caacb/tenor.gif |@{destroyer.name}| <center>{destroyer.score}</center>

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

</center>
<center>https://steemnova.intinte.org/</center>
https://steemnova.intinte.org/styles/resource/images/meta.png
""")
