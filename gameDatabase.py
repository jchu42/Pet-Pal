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
from config import load_config


def run_command (command : str | list[str]):
    con = psycopg2.connect(
        database='game_data',
        user='btran37',
        password='tk6cqTyGZK4I',
        host='ep-soft-breeze-a5w3y270.us-east-2.aws.neon.tech',
        port= '5432'
    )
    cursor_obj = con.cursor() 
    if type(command) == str:
        try:
            cursor_obj.execute(command)
        except (psycopg2.DatabaseError, Exception) as error:
            print("FERGFSR", error)
    else:
        for one_command in command:
            try:
                cursor_obj.execute(one_command)
            except (psycopg2.DatabaseError, Exception) as error:
                print("FERGFSR", error)
    con.commit()
    con.close()


def create_tables():

    """ Create tables in the PostgreSQL database"""
    run_command (["""CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL
        )""","""CREATE TABLE pets (
            pet_id SERIAL PRIMARY KEY,
            pet_type VARCHAR(255) NOT NULL,
            pet_happy INT,
            pet_action VARCHAR(255),
            poops JSONB[]
        )"""])

# for adding a user or pet
def add_user(user_name, user_password):
    run_command("INSERT INTO users (user_name, user_password) VALUES ('" + user_name + "', '" + user_password + "')")

def add_pet(pet_type, pet_happy, pet_action, poops):
    run_command("INSERT INTO pets (pet_type, pet_happy, pet_action, poops) VALUES ('" + pet_type + "', '" + str(pet_happy) + "', '" + pet_action + "', '" + str(len(poops)) + "')")

if __name__ == '__main__':
    create_tables()
    