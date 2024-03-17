"""This module contains database functions.
To reset the database, run this module."""

import psycopg2
import exceptions as err
from config import Config

class GameDatabase:
    """Contains functions to interact with the database"""
    @staticmethod
    def run_command (*args, **wargs)->tuple|None:
        """Connect to database and run the execute function with the given parameters
        
        Parameters
        ----------
        *args : tuple
            The arguments to give to cursor execute
        **wargs : dict
            The arguments to give to cursor execute

        Returns
        -------
        tuple
            One line of the results of the command
        None
            When the command did not return anything

        Raises
        ------
        pycopg2.DatabaseError
            Raised when the command fails to run
        """
        with psycopg2.connect(database=Config.config['Database']['database'],
                            user=Config.config['Database']['user'],
                            password=Config.config['Database']['password'],
                            host=Config.config['Database']['host'],
                            port= Config.config['Database']['port']
                            ) as con:
            cursor_obj = con.cursor()

            cursor_obj.execute(*args, **wargs)

            try:
                res = cursor_obj.fetchone()
            except psycopg2.ProgrammingError: # if execute did not return any data
                res = None
        con.close()

        return res
    @staticmethod
    def verify_user (username:str, password:str) -> bool:
        """Returns True if username+password combo exists in database
        
        Parameters
        ----------
        username : str
            The user's username
        password : str
            The user's password

        Returns
        -------
        bool
            True if the username+password combo matches in the database
        """
        command = """SELECT * FROM users WHERE user_name = %s AND user_password = %s"""
        values = (username, password)
        res = GameDatabase.run_command(command, values)
        return res is not None
    @staticmethod
    def add_user(user_name:str, user_password:str)->None:
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
        GameDatabase.run_command(command, values)

    USERNAME = "user_name"
    PET_TYPE = "pet_type"
    ROOM_TYPE = "room_type"
    BORDER_TYPE = "border_type"
    PET_HUNGER = "pet_hunger"
    POOPS = "poops"
    LAST_UPDATED = "last_updated"
    FIELD_OPTIONS = (USERNAME, PET_TYPE, ROOM_TYPE, BORDER_TYPE, PET_HUNGER, POOPS, LAST_UPDATED)

    @staticmethod
    def get_pet(username, fields:tuple|str)->tuple:
        """Get the selected fields from the database with the given username
        
        Parameters
        ----------
        fields : tuple|str
            The fields to get from the database
            options: pet_Type, room_Type, border_type, pet_hunger, poops, last_updated

        Returns
        -------
        tuple
            The received values from the database
        """
        if isinstance(fields, tuple):
            for field in fields:
                if field not in GameDatabase.FIELD_OPTIONS:
                    raise err.FieldNotFoundException("Unknown field: " + field)
            command = "SELECT " + (', '.join(fields)) + " FROM users WHERE user_name='" + username + "'"
        else:
            if fields not in GameDatabase.FIELD_OPTIONS:
                raise err.FieldNotFoundException("Unknown field: " + fields)
            command = "SELECT " + fields + " FROM users WHERE user_name='" + username + "'"
        ret = GameDatabase.run_command(command)
        return ret
    @staticmethod
    def set_pet(username:str,
                pet_type:str=None,
                room_type:str=None,
                border_type:str=None,
                pet_hunger:int=None,
                poops:int=None,
                last_updated:int=None
                )->None:
        """Set the particular fields to the values in the database
        
        Parameters
        ----------
        username : str, default=None
            The username to use with the database
        pet_type : str, default=None
            The pet the user selected. Keep as None to not change. 
        room_type : str, default=None
            The room type the user selected. Keep as None to not change.
        border_type : str, default=None
            The border type the user selected. Keep as None to not change.
        pet_hunger : int, default=None
            The hunger of the pet. Keep as None to not change.
        poops : int, default=None
            The number of poops the pet has taken. Keep as None to not change.
        last_updated : float, default=None
            The last time the pet's status was updated. Keep as None to not change.
        """
        command = "UPDATE users SET "
        data = [("pet_type", pet_type), 
                ("room_type", room_type),
                ("border_type", border_type),
                ("pet_hunger", pet_hunger),
                ("poops", poops),
                ("last_updated", last_updated)]
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
        GameDatabase.run_command(command)


if __name__ == '__main__':
    Config.load_config()
    GameDatabase.run_command("""DROP TABLE users""")

    GameDatabase.run_command ("""CREATE TABLE users (
                              user_name VARCHAR(255) PRIMARY KEY,
                              user_password VARCHAR(255) NOT NULL,
                              pet_type VARCHAR(255),
                              room_type VARCHAR(255),
                              border_type VARCHAR(255),
                              pet_hunger INT,
                              poops INT,
                              last_updated FLOAT(53)
                              )""")
    print ("Table reset.")
