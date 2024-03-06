# this file holds the rough code on how to connect python and postgres

## CITATION (the code below is referenced for the following link): https://www.youtube.com/watch?v=M2NzvnfS-hI


#step 1: in a terminal window type: pip3 install psycopg2

#step 2: in postgres account (assumming a new database is already made), 
#we'll need the following info:
#hostname  
#database 
#pwd
#port_id

########## To uncomment CTRL+K+U #######


####### IMPLEMENTATION BELOW ############

import psycopg2
import traceback
from config import load_config


def run_command (*args, **wargs)->tuple|None:
    con = psycopg2.connect(
        database='game_data',
        user='btran37',
        password='tk6cqTyGZK4I',
        host='ep-soft-breeze-a5w3y270.us-east-2.aws.neon.tech',
        port= '5432'
    )
    cursor_obj = con.cursor() 

    try:
        cursor_obj.execute(*args, **wargs)
    except psycopg2.DatabaseError:
        print("command error")
        traceback.print_exc()
    #if cursor_obj.rowcount > 0:
    try:
        res = cursor_obj.fetchone()
    except psycopg2.ProgrammingError: # if execute did not return any data
        res = None
    con.commit()
    con.close()

    return res

def verify_user (username, password) -> bool:
    """Returns True if username+password combo exists in database"""
    command = """SELECT * FROM users WHERE user_name = %s AND user_password = %s"""
    values = (username, password)
    res = run_command(command, values)
    return res is not None

# for adding a user or pet
def add_user(user_name, user_password):
    command = """INSERT INTO users (user_name, user_password, pet_type)
        VALUES (%s, %s, %s)
    """
    values = (user_name, user_password, "")
    run_command(command, values)

def get_pet(username)->tuple[str, str, int, int]:
    ret = run_command("SELECT pet_type, room_type, pet_happy, poops FROM users WHERE user_name='" + username + "'")
    print ("GET PET: ", ret)
    return ret

def set_pet(username, pet_type, room_type, pet_happy, poops):
    command = """UPDATE users
        SET pet_type = %s, room_type = %s, pet_happy = %s, poops = %s
        WHERE user_name = %s
        """
    values = (pet_type, room_type, pet_happy, poops, username)
    run_command(command, values)


if __name__ == '__main__':
    run_command("""DROP TABLE users""")

    run_command ("""CREATE TABLE users (
            user_name VARCHAR(255) PRIMARY KEY,
            user_password VARCHAR(255) NOT NULL,
            pet_type VARCHAR(255),
            room_type VARCHAR(255),
            pet_happy INT,
            poops INT
                    )""")