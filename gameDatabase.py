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

hostname = ''
database = ''
username = ''
pwd = ''
port_id = ''

conn = None
cur = None

try:
    conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)

#a cursor to perfor database operations
    cur = conn.cursor()

    create_script = ''' CREATE TABLE IF NOT EXISTS player (
                            id int PRIMARY KEY
                            username varchar(40) NOT NULL
                            password varchar(40) NOT NULL)'''
    cur.execute(create_script)

    #an example to insert a value into table player
    #the %s are palce holders
    insert_script = 'INSERT INTO player (id, username, password) VALUES (%s, %s, %s)'
    insert_value = (1, 'Yikes', 'pwd1234')

    cur.execute(insert_script, insert_value)

    ##Insert mulitple records

    ##FETCH data from PostgreSQL Table and display in Python program
    #cur.fetchall()

    ##UPDATE table record 

    conn.commit()
except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()