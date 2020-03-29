import mysql.connector
from mysql.connector import errorcode
from databases import config, local_config
import datetime


def updater(loc_table_name, table_name, id_, select, **rest):
    if rest != {}:
        stat_type = rest['stat_type']
        mycursor.execute(f"SELECT {id_},{select} FROM {table_name} WHERE stat_type={stat_type} ORDER BY {id_}")
    else:
        mycursor.execute(f"SELECT {id_},{select} FROM {table_name} ORDER BY {id_}")
    points = mycursor.fetchall()
    try:
        mycursor_loc.execute(f"ALTER TABLE `{loc_table_name}` ADD COLUMN `{today}` INT NULL AFTER `id`;")
        print("Import", loc_table_name, "started")
    except:
        print("Update", loc_table_name, "started")
    finally:
        for idek, point in points:
            if idek <= maxnewid:
                #Uncomment two lines below and comment UPDATE line only for first insert
                # mycursor_loc.execute(f"INSERT INTO {loc_table_name} VALUES({idek}, {point})")
                # print(f"{idek} {point}")
                mycursor_loc.execute(f"UPDATE {loc_table_name} SET `{today}` = {point} WHERE id={idek}")
                sql_loc.commit()
            else:
                mycursor_loc.execute(f"INSERT INTO {loc_table_name} (id, `{today}`) VALUES({idek},{point})")
                sql_loc.commit()
        print("Import/update", loc_table_name, "finished!")


date = datetime.datetime.now()
today = (date.strftime("%Y-%m-%d"))
print(today)
users_table = "sn1_users"

try:
    sql_loc = mysql.connector.connect(**local_config)
    mycursor_loc = sql_loc.cursor(buffered=True)
    print("Connection local database succesful!")
    mycursor_loc.execute(f"SELECT id FROM {users_table} ORDER BY id")
    ids = mycursor_loc.fetchall()
    maxnewid = ids[len(ids) - 1][0]

    sql = mysql.connector.connect(**config)
    mycursor = sql.cursor(buffered=True)
    mycursor2 = sql.cursor(buffered=True)
    print("Connection steemnova database succesful!")
    mycursor.execute("SELECT id_owner,total_points FROM uni1_statpoints WHERE stat_type=1 ORDER BY id_owner")
    points = mycursor.fetchall()

    # POINTS
    try:
        mycursor_loc.execute(f"ALTER TABLE `{users_table}` ADD COLUMN `{today}` INT NULL AFTER `name`;")
        print(f"Import {users_table} started")
    except:
        print(f"UPDATE {users_table} started")
    finally:
        for idek, point in points:
            if idek <= maxnewid:
                mycursor_loc.execute(f"UPDATE {users_table} SET `{today}` = {point} WHERE id={idek}")
                sql_loc.commit()
            else:
                # adding new players to the table
                mycursor2.execute(f"SELECT username FROM uni1_users WHERE id={idek}")
                name = mycursor2.fetchall()[0][0]
                mycursor_loc.execute(
                    f"INSERT INTO {users_table} (id, name, `{today}`) VALUES({idek},\"{name}\",{point})")
                print(f"Added to database: {idek} {name} {point}")
                sql_loc.commit()
        print(f"Import {users_table} finished!")

    # AGRESOR
    updater("sn1_agresor", "uni1_users", "id", "wons")

    # BUNKER
    updater("sn1_bunker", "uni1_statpoints", "id_owner", "defs_points", stat_type=1)

    # DESTROYER
    updater("sn1_destroyer", "uni1_users", "id", "desunits")

    # FAIL and BUILDER
    updater("sn1_fail", "uni1_statpoints", "id_owner", "fleet_points", stat_type=1)

    # FARM
    updater("sn1_farm", "uni1_users", "id", "loos")

    print("Import completed")
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    sql.close()
    sql_loc.close()

