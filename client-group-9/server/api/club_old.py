import psycopg2
import yaml
import os
import pandas as pd
import numpy as np
import sys
import os
from .swen610_db_utils import *

def rebuild_tables():
    exec_sql_file('schema.sql')
    exec_sql_file('test_data.sql')

###########################################################
#------------------ login functions ------------------------ 
###########################################################

def login_check(user, password):
    """matches username and passowrd in database and return list of tupple of size one if found. 
    
    access: developer

    arguments:
    user -- name of the user
    pass -- password of the user
    """
    result = exec_get_all(''' 
                            SELECT *
                            FROM users 
                            WHERE users.name = %s and users.password =%s ''', (user,password))
    return result

def login_user(**kwargs):
    """login user and return session id if successful. 
    
    access: developer

    kewword arguments:
    name -- name of the user
    pass -- password of the user
    """
    result = login_check(key_exists('name', **kwargs), key_exists('password', **kwargs))
    if (len(result) == 1):
        session_id = session_id_gen(1000)
        update_session_id(key_exists('name', **kwargs), session_id)
        return session_id
    else:
        return 'Name or password is incorrect'

def authenticate_seesion_id(name, session_id):
    """authenticate session id. 
    
    access: developer

    kewword arguments:
    name -- name of the user
    session_id -- session id  of the user
    """
    result = exec_get_all(''' 
                            SELECT *
                            FROM users 
                            WHERE users.name = %s and users.session_id =%s ''', (name,session_id))
    return result

def update_session_id(user, id):
    """update session_id of user. 
    
    access: developer

    arguments:
    user -- old name of the user
    id -- session ID
    """
    result = exec_commit('''UPDATE users 
                            SET session_id = %s 
                            WHERE name = %s
                            ''', (id, user))    
    return result


###########################################################
#------------------ user functions ------------------------ 
###########################################################

def list_users():
    """return all users as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT name
                            FROM users ''')
    return result

def user_exist(user):
    """check user existnace in database and return list of tupple of size one if found. 
    
    access: developer

    arguments:
    user -- name of the user
    """
    result = exec_get_all(''' 
                            SELECT name, age, email
                            FROM users 
                            WHERE users.name = %s  ''', (user,))
    return result

def insert_user(**kwargs):
    """insert user in database and return  list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    name -- name of the user
    pass -- password of the user
    email -- email of the user
    age  -- age of the user
    created_at -- date when the user was created (default NOW())
    last_modified_at -- date when any of the field of the user was modified (default NOW())
    """

    result = user_exist(key_exists('name', **kwargs))

    if(len(result)==1):
        result = key_exists('name', **kwargs) + ' already exists'
        return result
    else: 
        result = exec_commit('''INSERT INTO users(name, password, email, age) 
                            VALUES (%s,%s,%s,%s)''', 
                            (key_exists('name', **kwargs), key_exists('password', **kwargs),
                            key_exists('email', **kwargs), key_exists('age', **kwargs)))
                            
        result = user_exist(key_exists('name', **kwargs))
    
        return result

def del_user(**kwargs):
    """delete user in database and return  an emply list if successful. 
    
    access: developer

    kewword arguments:
    name -- name of the user
    session_id -- session_id of the user
    """

    result = user_exist(key_exists('name', **kwargs))


    if(len(result)==0):
        result = key_exists('name', **kwargs) + ' doesnot exists'
        return result
    else: 
        result = exec_commit('''DELETE FROM users WHERE name = %s and session_id = %s''', 
                            (key_exists('name', **kwargs), key_exists('session_id', **kwargs)))                    
        result = user_exist(key_exists('name', **kwargs))
    
        return result

def update_user_info(**kwargs):
    """update information of user in the database.
    
    access: developer

    kewword arguments:
    name -- name of the user
    session_id -- session of the user
    email -- new email of the user
    age -- age of the user
    """

    result = user_exist(key_exists('name', **kwargs))

    if(len(result)==0):
        result = key_exists('name', **kwargs) + ' doesnot exists'
        return result
    else: 
        result = exec_commit('''UPDATE users 
                                SET email = %s , age = %s
                                WHERE name = %s and session_id = %s
                                ''', (key_exists('email', **kwargs), key_exists('age', **kwargs), 
                                key_exists('name', **kwargs), key_exists('session_id', **kwargs)))    
        
        result = user_exist(key_exists('name', **kwargs))
        return result


###########################################################
#--------------- manager functions --------------------- 
###########################################################

def list_managers():
    """return all managers as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT user_name, club_name
                            FROM managers ''')
    return result

def insert_manager(**kwargs):
    """insert manager of the club in database and return list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of manager
    club_name -- name of the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('user_name', **kwargs))
    if(len(result)==0):
        result = key_exists('user_name', **kwargs) + ' doesnot exists'
        return result

    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(len(result)==1):
        result = key_exists('club_name', **kwargs) + ' already has a manager'
        return result

    result = get_managers_club(key_exists('user_name', **kwargs))
    if(len(result)==1):
        result = key_exists('user_name', **kwargs) + ' is already a manager of another club'
        return result

    result = exec_commit('''INSERT INTO managers(user_name, club_name) 
                            VALUES (%s,%s)''', 
                            (key_exists('user_name', **kwargs), key_exists('club_name', **kwargs)))
                            
    result = get_clubs_manager(key_exists('club_name', **kwargs))
    return result

def update_manager(**kwargs):
    """update manager of the club in database and return list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of manager
    club_name -- name of the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('user_name', **kwargs))
    if(len(result)==0):
        result = key_exists('user_name', **kwargs) + ' doesnot exists'
        return result

    result = get_managers_club(key_exists('user_name', **kwargs))
    if(len(result)==1):
        result = key_exists('user_name', **kwargs) + ' is already a manager of another club'
        return result

    result = exec_commit('''UPDATE managers SET user_name =%s 
                            WHERE club_name = %s''', 
                            (key_exists('user_name', **kwargs), key_exists('club_name', **kwargs)))
                            
    result = get_clubs_manager(key_exists('club_name', **kwargs))
    return result

def del_manager(**kwargs):
    """del manager of the club in database and return list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of manager
    club_name -- name of the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' has no manager'
        return result
    
    if(result != [(key_exists('user_name', **kwargs),)]):
        result = key_exists('user_name', **kwargs) + ' is not the manager of ' + key_exists('club_name', **kwargs)
        return result

    if(result == [(key_exists('user_name', **kwargs),)]):
        result = exec_commit('''Delete FROM managers 
                                where club_name =%s and user_name = %s ''', 
                                (key_exists('club_name', **kwargs), key_exists('user_name', **kwargs)))
                                
        result = get_clubs_manager(key_exists('club_name', **kwargs))
        return result
    
def get_clubs_manager(club):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    club -- name of the club
    """
    result = exec_get_all(''' 
                            SELECT user_name
                            FROM managers
                            WHERE managers.club_name = %s ''', (club,))
    return result

def get_managers_club(name):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    name -- name of the manager
    """
    result = exec_get_all(''' 
                            SELECT club_name
                            FROM managers
                            WHERE user_name = %s ''', (name,))
    return result

###########################################################
#--------------- bouncer functions --------------------- 
###########################################################

def list_bouncers():
    """return all managers as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT user_name, club_name
                            FROM bouncers ''')
    return result

def insert_bouncer(**kwargs):
    """insert bouncer of the club in database and return  list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of bouncer
    club_name -- name of the club
    manager_name -- name of the manager
    session_id -- session id of manager
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('user_name', **kwargs))
    if(len(result)==0):
        result = key_exists('user_name', **kwargs) + ' doesnot exists'
        return result
    
    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(result != [(key_exists('manager_name', **kwargs),)]):
        result = key_exists('manager_name', **kwargs) + ' is not the manager of ' + key_exists('club_name', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('manager_name', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result

    result = get_bouncers_club(key_exists('user_name', **kwargs))
    if(len(result)==1):
        result = key_exists('user_name', **kwargs) + ' is already a bouncer of another club'
        return result

    result = exec_commit('''INSERT INTO bouncers(user_name, club_name) 
                            VALUES (%s,%s)''', 
                            (key_exists('user_name', **kwargs), key_exists('club_name', **kwargs)))
                            
    result = get_clubs_bouncer(key_exists('club_name', **kwargs))
    return result

def del_bouncer(**kwargs):
    """del bouncer of the club in database and return  list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of bouncer
    club_name -- name of the club
    manager_name -- name of the manager
    session_id -- session id of manager
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('user_name', **kwargs))
    if(len(result)==0):
        result = key_exists('user_name', **kwargs) + ' doesnot exists'
        return result
    
    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(result != [(key_exists('manager_name', **kwargs),)]):
        result = key_exists('manager_name', **kwargs) + ' is not the manager of ' + key_exists('club_name', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('manager_name', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result

    result = get_bouncers_club(key_exists('user_name', **kwargs))
    if(result != [(key_exists('club_name', **kwargs),)]):
        result = key_exists('user_name', **kwargs) + ' is not a bouncer of ' + key_exists('club_name', **kwargs)
        return result

    result = exec_commit('''Delete from bouncers where user_name = %s and club_name = %s''', 
                            (key_exists('user_name', **kwargs), key_exists('club_name', **kwargs)))
                            
    result = get_clubs_bouncer(key_exists('club_name', **kwargs))
    return result

def get_bouncers_club(name):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    name -- name of the bouncer
    """
    result = exec_get_all(''' 
                            SELECT club_name
                            FROM bouncers
                            WHERE user_name = %s ''', (name,))
    return result

def get_clubs_bouncer(club):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    club -- name of the club
    """
    result = exec_get_all(''' 
                            SELECT user_name
                            FROM bouncers
                            WHERE club_name = %s ''', (club,))
    return result


##########################################################
#------------------ club functions ------------------------ 
###########################################################

def list_clubs():
    """return all clubs as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT name,capacity,city 
                            FROM clubs ''')
    return result

def get_club_capacity(club_name):
    """return all clubs as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT capacity 
                            FROM clubs 
                            where name= %s''', (club_name,))
    return result

def club_exist(club):
    """check user existnace in database and return list of tupple of size one if found. 
    
    access: developer

    arguments:
    club -- club of the user
    """
    result = exec_get_all(''' 
                            SELECT name, capacity, city
                            FROM clubs 
                            WHERE clubs.name = %s  ''', (club,))
    return result

def insert_club(**kwargs):
    """insert club in database and return  list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    name -- name of the club
    capacity -- capacity of club
    city -- city of club
    opening_time -- opening time of club, 
    closing_time -- closing time of club, 
    created_at -- date when the user was created (default NOW())
    last_modified_at -- date when any of the field of the user was modified (default NOW())
    """

    result = club_exist(key_exists('name', **kwargs))

    if(len(result)==1):
        result = key_exists('name', **kwargs) + ' already exists'
        return result
    else: 
        result = exec_commit('''INSERT INTO clubs(name, capacity, city, opening_time, closing_time) 
                            VALUES (%s,%s,%s,%s,%s)''', 
                            (key_exists('name', **kwargs), key_exists('capacity', **kwargs),
                            key_exists('city', **kwargs), key_exists('opening_time', **kwargs),
                            key_exists('closing_time', **kwargs) ))
                            
        result = club_exist(key_exists('name', **kwargs))
        return result

def update_club(**kwargs):
    """update information of club in the database.
    
    access: developer

    kewword arguments:
    manager_name -- name of manager of the club
    session_id -- session id of the manager
    club_name -- name of the club
    session_id -- session id of the club
    capacity -- capacity of the club
    city -- city of the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('manager_name', **kwargs))
    if(len(result)==0):
        result = key_exists('manager_name', **kwargs) + ' doesnot exists'
        return result

    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(result != [(key_exists('manager_name', **kwargs),)]):
        result = key_exists('manager_name', **kwargs) + ' is not the manager of ' + key_exists('club_name', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('manager_name', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result

    result = exec_commit('''UPDATE clubs SET capacity = %s , city = %s, opening_time= %s, closing_time =%s
                            WHERE name = %s ''', 
                            (key_exists('capacity', **kwargs),key_exists('city', **kwargs), 
                            key_exists('opening_time', **kwargs), key_exists('closing_time', **kwargs), 
                            key_exists('club_name', **kwargs))) 
            
    result = club_exist(key_exists('club_name', **kwargs))
    return result

def del_club(**kwargs):
    """update information of club in the database.
    
    access: developer

    kewword arguments:
    manager_name -- name of manager of the club
    session_id -- session id of the manager
    club_name -- name of the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('manager_name', **kwargs))
    if(len(result)==0):
        result = key_exists('manager_name', **kwargs) + ' doesnot exists'
        return result

    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(result != [(key_exists('manager_name', **kwargs),)]):
        result = key_exists('manager_name', **kwargs) + ' is not the manager of ' + key_exists('club_name', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('manager_name', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result

    result = exec_commit('''Delete from clubs where name = %s ''' 
                            , (key_exists('club_name', **kwargs),)) 
            
    result = club_exist(key_exists('club_name', **kwargs))

    return result

##########################################################
#------------------ Entry functions ----------------------
###########################################################

def enter_club(**kwargs):
    """enter users to the club.
    
    access: Bouncers

    kewword arguments:
    bouncer_name -- name of bouncer of the club
    session_id -- session id of the bouncer
    club_name -- name of the club
    user_name -- name of the person adding the club
    entry_time -- time at which person is entering the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('bouncer_name', **kwargs))
    if(len(result)==0):
        result = key_exists('bouncer_name', **kwargs) + ' doesnot exists'
        return result

    result = get_bouncers_club(key_exists('bouncer_name', **kwargs))
    if(result != [(key_exists('club_name', **kwargs),)]):
        result = key_exists('bouncer_name', **kwargs) + ' is not the bouncer of ' + key_exists('club_name', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('bouncer_name', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'bouncer needs to login to allow entry to club'
        return result

    result = get_entry(key_exists('club_name', **kwargs),key_exists('user_name', **kwargs)) 
    if (len(result)==1):
        return key_exists('user_name', **kwargs) + ' is already in the club'

    current_count = get_current_entries_in_club(key_exists('club_name', **kwargs),key_exists('enter_time', **kwargs) )
    capacity = get_club_capacity(key_exists('club_name', **kwargs))

    if (current_count<capacity):
        result = exec_commit('''INSERT INTO entered(user_name, club_name, enter_time, left_time, amount_spent) 
                                VALUES (%s,%s,%s,%s,%s)''', 
                                (key_exists('user_name', **kwargs), key_exists('club_name', **kwargs),
                                key_exists('enter_time', **kwargs),key_exists('left_time', **kwargs), 
                                key_exists('amount_spent', **kwargs))) 

        result = get_current_entries_in_club(key_exists('club_name', **kwargs),key_exists('enter_time', **kwargs) )
        return result
    else:
        return 'club is at full capacity, cant enter'

def leave_club(**kwargs):
    """enter users to the club.
    
    access: Bouncers

    kewword arguments:
    club_name -- name of the club
    user_name -- name of the person adding the club
    amount_spent -- the amount person spent in the club
    left_time -- time at which person is leaving the club
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    entry = get_entry(key_exists('club_name', **kwargs), key_exists('user_name', **kwargs))
    if(len(entry)==0):
        result = key_exists('user_name', **kwargs) +' is not present in the club'
        return result

    result = exec_commit('''UPDATE entered SET left_time=%s, amount_spent=%s 
                            Where id =%s''', 
                            (key_exists('left_time', **kwargs), key_exists('amount_spent', **kwargs),entry[0][0])) 

    result = get_entry(key_exists('club_name', **kwargs), key_exists('user_name', **kwargs))
    return result

def get_entry(club_name, user_name):
    """return the record if user is preseent in the club.
    
    access: eveloper

    arguments:
    club_name -- name of the club
    user_name -- name of the person adding the club
    """
    result = exec_get_all('''SELECT *
                            FROM entered
                            WHERE user_name = %s and club_name= %s and left_time is null''', 
                            (user_name, club_name)) 

    return result

def get_current_entries_in_club(club_name, enter_time):
    """return all the entries for a given date and club.
    
    access: eveloper

    arguments:
    club_name -- name of the club
    enter_time -- time of entry into the club
    """
    result = exec_get_all('''SELECT count(id)
                            FROM entered
                            WHERE club_name= %s and date(enter_time) = date(%s)''', 
                            (club_name,enter_time)) 

    return result

def get_entries_in_club(club_name):
    """return all entries (past + present) that match club_name .
    
    access: eveloper

    arguments:
    club_name -- name of the club
    enter_time -- time of entry into the club
    """
    result = exec_get_all('''SELECT *
                            FROM entered''', 
                            (club_name,)) 
    return result


##########################################################
#------------------ INFO functions ----------------------
###########################################################

def club_info(**kwargs):
    """enter users to the club.
    
    access: Bouncers

    kewword arguments:
    club_name -- name of the club
    date -- date for which info is required(optional)
    """

    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        result = key_exists('club_name', **kwargs) + ' doesnot exists'
        return result

    if (key_exists('date', **kwargs) == ''):
        result = exec_get_all('''select SUM(amount_spent) as income, count(id) as population
                                FROM entered WHERE club_name = %s''', 
                                (key_exists('club_name', **kwargs),)) 

        return result
    else:
        result = exec_get_all('''select SUM(amount_spent) as income, count(id) as population
                                FROM entered WHERE club_name = %s and date(enter_time) = date(%s)''', 
                                (key_exists('club_name', **kwargs),
                                key_exists('date', **kwargs)))

        return result

##########################################################
#------------------ Filter functions ----------------------
###########################################################

def club_filter(**kwargs):
    """filter club according to income and population.
    
    access: Bouncers

    kewword arguments:
    income -- minimum income of club
    population -- minimum population of club
    """


    if (key_exists('population', **kwargs) == 0):
        result = exec_get_all('''select club_name, SUM(amount_spent) as income, count(id) as population
                                FROM entered
                                Group BY club_name
                                having SUM(amount_spent)>= %s''',
                                (key_exists('income', **kwargs),)) 

        return result

    if (key_exists('income', **kwargs) == 0):
        result = exec_get_all('''select club_name, SUM(amount_spent) as income, count(id) as population
                                FROM entered
                                Group BY club_name
                                having count(id) >=%s ''',
                                (key_exists('population', **kwargs), )) 

        return result

    if (key_exists('income', **kwargs) == 0 and key_exists('population', **kwargs) == 0) :
        result = exec_get_all('''select club_name, SUM(amount_spent) as income, count(id) as population
                                FROM entered
                                Group BY club_name
                                having SUM(amount_spent)>= %s and count(id) >=%s''') 

    else:
        result = exec_get_all('''select club_name, SUM(amount_spent) as income, count(id) as population
                                FROM entered
                                Group BY club_name
                                having SUM(amount_spent)>= %s and count(id) >=%s ''',
                                (key_exists('income', **kwargs),key_exists('population', **kwargs))) 
        
        return result