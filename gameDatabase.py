"""This module contains database functions"""

import traceback
import psycopg2
import exceptions as err

def run_command (*args, **wargs)->tuple|None:
    """Connect to database and run the execute function with the given parameters
    
    Parameters
    ----------
    *args : tuple
        The arguments to give to cursor execute
    **wargs : dict
        The arguments to give to cursor execute
    """
    with psycopg2.connect(database='game_data',
                          user='btran37',
                          password='tk6cqTyGZK4I',
                          host='ep-soft-breeze-a5w3y270.us-east-2.aws.neon.tech',
                          port= '5432'
                          ) as con:
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
    con.close()

    return res

def verify_user (username, password) -> bool:
    """Returns True if username+password combo exists in database"""
    command = """SELECT * FROM users WHERE user_name = %s AND user_password = %s"""
    values = (username, password)
    res = run_command(command, values)
    return res is not None

# for adding a user or pet
def add_user(user_name, user_password)->None:
    """Add the username+password combination to the database as a new user with empty data
    
    Parameters
    ----------
    user_name : str
        The user's chosen username
    user_password : str
        The user's chosen password
    """
    command = """INSERT INTO users (user_name, user_password, pet_type)
        VALUES (%s, %s, %s)
    """
    values = (user_name, user_password, "")
    run_command(command, values)

USERNAME = "user_name"
PET_TYPE = "pet_type"
ROOM_TYPE = "room_type"
BORDER_TYPE = "border_type"
PET_HAPPY = "pet_happy"
POOPS = "poops"
FIELD_OPTIONS = (USERNAME, PET_TYPE, ROOM_TYPE, BORDER_TYPE, PET_HAPPY, POOPS)

def get_pet(username, fields:tuple)->tuple:
    """Get the selected fields from the database with the given username
    
    Parameters
    ----------
    fields : tuple
        The fields to get from the database
        options: pet_Type, room_Type, border_type, pet_happy, poops

    Returns
    -------
    tuple
        The received values from the database
    """
    if isinstance(fields, tuple):
        for field in fields:
            if field not in FIELD_OPTIONS:
                raise err.FieldNotFoundException("Unknown field: " + field)
        command = "SELECT " + (', '.join(fields)) + " FROM users WHERE user_name='" + username + "'"
    else:
        if fields not in FIELD_OPTIONS:
            raise err.FieldNotFoundException("Unknown field: " + fields)
        command = "SELECT " + fields + " FROM users WHERE user_name='" + username + "'"
    ret = run_command(command)
    print ("GET PET: ", ret)
    return ret

def set_pet(username, pet_type:str=None, room_type:str=None, border_type:str=None, pet_happy:int=None, poops:int=None)->None:
    """Set the particular fields to the values in the database
    
    Parameters
    ----------
    pet_type : str
    room_type : str
    border_type : str
    pet_happy : int
    poops : int
    """
    command = "UPDATE users SET "
    data = [("pet_type", pet_type), 
            ("room_type", room_type),
            ("border_type", border_type),
            ("pet_happy", pet_happy),
            ("poops", poops)]
    prev_used:bool = False
    for param, val in data:
        if val is not None:
            if prev_used:
                command += ", "
            command += param + " = "
            if isinstance(val, str):
                command += "'" + val + "'"
            else:
                command += str(val)
            prev_used = True
    command += " WHERE user_name = '" + username + "'"
    run_command(command)


if __name__ == '__main__':
    run_command("""DROP TABLE users""")

    run_command ("""CREATE TABLE users (
            user_name VARCHAR(255) PRIMARY KEY,
            user_password VARCHAR(255) NOT NULL,
            pet_type VARCHAR(255),
            room_type VARCHAR(255),
            border_type VARCHAR(255),
            pet_happy INT,
            poops INT
                    )""")