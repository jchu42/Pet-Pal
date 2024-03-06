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

# if you have your old postgres acc info it would go here 
con = psycopg2.connect(
database='game_data',
user='btran37',
password='tk6cqTyGZK4I',
host='ep-soft-breeze-a5w3y270.us-east-2.aws.neon.tech',
port= '5432'
)

cursor_obj = con.cursor() 

#print(cursor_obj.fetchall())

#cursor_obj.execute("SELECT * FROM game_data")

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_password VARCHAR(255) NOT NULL
        )""",
        """CREATE TABLE pets (
            pet_id SERIAL PRIMARY KEY,
            pet_type VARCHAR(255) NOT NULL,
            pet_happy INT,
            pet_action VARCHAR(255),
            poops JSONB[]
        )"""
    )
    try:
        config = load_config()  # Load the configuration
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# for adding a user or pet
def add_user(user_name, user_password):
    """Add a new user to the users table."""
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (user_name, user_password) VALUES (%s, %s)", (user_name, user_password))
                conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def add_pet(pet_type, pet_happy, pet_action, poops):
    """Add a new pet to the pets table."""
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO pets (pet_type, pet_happy, pet_action, poops) VALUES (%s, %s, %s, %s)", (pet_type, pet_happy, pet_action, poops))
                con.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        con.commit()
    con.close()
    # except Exception as error:
    #     print(error)
    # finally:
    #     if cur is not None:
    #         cur.close()
    #     if con is not None:
    #         con.close()

if __name__ == '__main__':
    create_tables()
    