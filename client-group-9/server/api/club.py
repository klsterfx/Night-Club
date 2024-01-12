import psycopg2
import yaml
import os
import pandas as pd
import numpy as np
import sys
import os
from .swen610_db_utils import *
from datetime import datetime

def rebuild_tables():
    exec_sql_file('club.sql')

###########################################################
#------------------ login functions ------------------------ 
###########################################################

def login_check(user, password):
    """matches username and passowrd in database and return list of tupple of size one if found. 
    
    access: developer

    arguments:
    user -- email of the user
    pass -- password of the user
    """

    result = exec_get_all(''' 
                            SELECT role
                            FROM users 
                            WHERE users.email = %s and users.password =%s ''', (user,password))
    return result

def login_user(**kwargs):
    """login user and return session id if successful. 
    
    access: developer

    kewword arguments:
    name -- name of the user
    pass -- password of the user
    """
    role = login_check(key_exists('email', **kwargs), key_exists('password', **kwargs))
    if (len(role) == 1):
        session_id = session_id_gen(1000)
        update_session_id(key_exists('email', **kwargs), session_id)
        return [session_id, role[0][0]]
    else:
        return 'email or password is incorrect'

def authenticate_seesion_id(email, session_id):
    """authenticate session id. 
    
    access: developer

    kewword arguments:
    name -- name of the user
    session_id -- session id  of the user
    """
    result = exec_get_all(''' 
                            SELECT *
                            FROM users 
                            WHERE users.email = %s and users.session_id= %s  ''', (email,session_id))
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
                            WHERE email = %s
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
                            SELECT *
                            FROM users 
                            where role = %s or role = %s ''', ( 'customer','user'))

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
                            WHERE users.email = %s  ''', (user,))
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

    result = user_exist(key_exists('email', **kwargs))

    if(len(result)==1):
        result = key_exists('email', **kwargs) + ' already exists'
        return result
    else: 
        result = exec_commit('''INSERT INTO users(name, password, email, age, city) 
                            VALUES (%s,%s,%s,%s,%s)''', 
                            (key_exists('name', **kwargs), key_exists('password', **kwargs),
                            key_exists('email', **kwargs), key_exists('age', **kwargs), key_exists('city', **kwargs)))
                            
        result = user_exist(key_exists('email', **kwargs))
        if (len(result)==1):
            return 'Account is created successfully'

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
                            SELECT club, email
                            FROM managers ''')
    return result

def insert_manager(**kwargs):
    """insert manager of the club in database and return list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of manager
    club_name -- name of the club
    """

    result = club_exist(key_exists('club', **kwargs))
    if(len(result)==0):
        result = key_exists('club', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('email', **kwargs))
    if(len(result)==0):
        result = key_exists('email', **kwargs) + ' doesnot exists'
        return result

    result = get_clubs_manager(key_exists('club', **kwargs))
    if(len(result)==1):
        result = key_exists('club', **kwargs) + ' already has a manager'
        return result

    result = get_managers_club(key_exists('email', **kwargs))
    if(len(result)==1):
        result = key_exists('email', **kwargs) + ' is a manager of another club'
        return result

    result = exec_commit('''INSERT INTO managers(email, club) 
                            VALUES (%s,%s)''', 
                            (key_exists('email', **kwargs), key_exists('club', **kwargs)))

    result = exec_commit('''UPDATE users SET role=%s
                            where email=%s''', 
                            ('manager', key_exists('email', **kwargs)))
                            
    result = get_clubs_manager(key_exists('club', **kwargs))
    if(len(result)==1):
        return "manager added successfully"

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

    manager = get_clubs_manager(key_exists('club_name', **kwargs))

   
    result = exec_commit('''Delete FROM managers 
                                where club =%s ''', 
                                (key_exists('club_name', **kwargs),))
    
    result = exec_commit('''UPDATE users SET role=%s
                            where email=%s''', 
                            ('user', manager[0][0]))
                                
    
    result = get_clubs_manager(key_exists('club_name', **kwargs))
    if(len(result)==0):
        return "manager deleted successfully"
    
def get_clubs_manager(club):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    club -- name of the club
    """
    result = exec_get_all(''' 
                            SELECT email
                            FROM managers
                            WHERE managers.club = %s ''', (club,))
    return result

def get_managers_club(email):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    name -- name of the manager
    """
    result = exec_get_all(''' 
                            SELECT club
                            FROM managers
                            WHERE email = %s ''', (email,))
    
    if(len(result)==1):
        result = exec_get_all(''' SELECT *
                            FROM clubs 
                            WHERE name= %s ''', (result[0][0], ))
        return result
    
    return result

###########################################################
#--------------- bouncer functions --------------------- 
###########################################################

def list_bouncers(club):
    """return all managers as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT club, email
                            FROM bouncers 
                            where club=%s
                             ''', (club,))
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

    result = club_exist(key_exists('club', **kwargs))
    if(len(result)==0):
        result = key_exists('club', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('email', **kwargs))
    if(len(result)==0):
        result = key_exists('email', **kwargs) + ' doesnot exists'
        return result
    
    result = get_clubs_manager(key_exists('club', **kwargs))

    if(result != [(key_exists('manager_email', **kwargs),)]):
        result = key_exists('manager_email', **kwargs) + ' is not the manager of ' + key_exists('club', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('manager_email', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result

    result = get_bouncers_club(key_exists('email', **kwargs))
    if(len(result)==1):
        result = key_exists('email', **kwargs) + ' is already a bouncer of another club'
        return result

    result = exec_commit('''INSERT INTO bouncers(email, club) 
                            VALUES (%s,%s)''', 
                            (key_exists('email', **kwargs), key_exists('club', **kwargs)))
                            
    result = exec_commit('''UPDATE users SET role=%s
                            where email=%s''', 
                            ('bouncer', key_exists('email', **kwargs)))
    result = get_clubs_bouncer(key_exists('club', **kwargs))

    if(len(result)>=1):
        return "bouncer added successfully"

def del_bouncer(**kwargs):
    """del bouncer of the club in database and return  list of tupple of size one if successful. 
    
    access: developer

    kewword arguments:
    user_name -- name of bouncer
    club_name -- name of the club
    manager_name -- name of the manager
    session_id -- session id of manager
    """

    club = get_bouncers_club(key_exists('email', **kwargs))
    if(len(club)==0):
        return  key_exists('email', **kwargs) +' is not a bouncer'

    clubname=club[0][0]
    result = club_exist(clubname)
    if(len(result)==0):
        result = clubname + ' doesnot exists'
        return result

    club = get_bouncers_club(key_exists('email', **kwargs))
    

    result = user_exist(key_exists('email', **kwargs))
    if(len(result)==0):
        result = key_exists('email', **kwargs) + ' doesnot exists'
        return result
    
    result = get_clubs_manager(clubname)
    if(result != [(key_exists('manager_email', **kwargs),)]):
        result = key_exists('manager_email', **kwargs) + ' is not the manager of ' + clubname
        return result

    result = authenticate_seesion_id(key_exists('manager_email', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result

    result = get_bouncers_club(key_exists('email', **kwargs))
    if(result[0][0] != clubname):
        result = key_exists('email', **kwargs) + ' is not a bouncer of ' + clubname
        return result

    result = exec_commit('''Delete from bouncers where email = %s and club = %s''', 
                            (key_exists('email', **kwargs), clubname))
                            
    result = exec_commit('''UPDATE users SET role=%s
                            where email=%s''', 
                            ('user',key_exists('email', **kwargs)))
    result = get_bouncers_club(key_exists('email', **kwargs))
    if(len(result)==0):
        return "bouncer deleted successfully"


def get_bouncers_club(email):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    name -- name of the manager
    """
    result = exec_get_all(''' 
                            SELECT club
                            FROM bouncers
                            WHERE email = %s ''', (email,))

    if(len(result)==1):
        result = exec_get_all(''' SELECT *
                            FROM clubs 
                            WHERE name= %s ''', (result[0][0], ))
        return result
    
    return result

def get_clubs_bouncer(club):
    """return all clubs as a list of tupple. 
    
    access: developer

    arguments:
    club -- name of the club
    """
    result = exec_get_all(''' 
                            SELECT email
                            FROM bouncers
                            WHERE bouncers.club = %s ''', (club,))
    return result


##########################################################
#------------------ club functions ------------------------ 
###########################################################

def list_clubs():
    """return all clubs as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT *
                            FROM clubs
                            order by clubs.name  ''')
    return result

def get_club_locations():
    """return all clubs as a list of tupple. 
    
    access: developer
    """
    result = exec_get_all(''' 
                            SELECT distinct(city)
                            FROM clubs
                            ''')
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
                            WHERE clubs.name = %s ''', (club,))
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
        result = key_exists('name', **kwargs) + ' already exists. select different name.'
        return result
    else: 
        result = exec_commit('''INSERT INTO clubs(name, city, music, capacity, yellow_threshold, current_count, increment, decrement) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', 
                            (key_exists('name', **kwargs), key_exists('city', **kwargs), key_exists('music', **kwargs),
                            key_exists('capacity', **kwargs), key_exists('yellow_threshold', **kwargs), key_exists('count', **kwargs), 
                             key_exists('increment', **kwargs),key_exists('decrement', **kwargs) ))
                            
        result = club_exist(key_exists('name', **kwargs))
        if(len(result)==1):
            return "club added successfully"

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

    result = club_exist(key_exists('oldname', **kwargs))
    if(len(result)==0):
        result = key_exists('oldname', **kwargs) + ' doesnot exists'
        return result


    result = get_clubs_manager(key_exists('oldname', **kwargs))
    if(result != [(key_exists('manager_email', **kwargs),)]):
        result = key_exists('manager_email', **kwargs) + ' is not the manager of ' + key_exists('oldname', **kwargs)
        return result

    if (key_exists('name', **kwargs) != key_exists('oldname', **kwargs)):
        result = club_exist(key_exists('name', **kwargs))
        if(len(result)==1):
            result = key_exists('name', **kwargs) + ' already exists'
            return result

    result = authenticate_seesion_id(key_exists('manager_email', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'manager needs to login to modify club details'
        return result


    result = exec_commit('''UPDATE clubs SET  name=%s, city =%s, music=%s, capacity = %s, yellow_threshold=%s,
                            current_count = %s, increment= %s, decrement =%s
                            WHERE name = %s ''', 
                            (key_exists('name', **kwargs), key_exists('city', **kwargs), key_exists('music', **kwargs),
                             key_exists('capacity', **kwargs), key_exists('yellow_threshold', **kwargs), key_exists('count', **kwargs), 
                             key_exists('increment', **kwargs),key_exists('decrement', **kwargs), key_exists('oldname', **kwargs))) 
            
    result = club_exist(key_exists('name', **kwargs))
    if(len(result)==1):
        return 'information modified successfully'

def update_club_customer(**kwargs):
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

    result = club_exist(key_exists('oldname', **kwargs))
    if(len(result)==0):
        result = key_exists('oldname', **kwargs) + ' doesnot exists'
        return result


    result = exec_commit('''UPDATE clubs SET  name=%s, city =%s, music=%s, capacity = %s, yellow_threshold=%s,
                            current_count = %s, increment= %s, decrement =%s
                            WHERE name = %s ''', 
                            (key_exists('name', **kwargs), key_exists('city', **kwargs), key_exists('music', **kwargs),
                             key_exists('capacity', **kwargs), key_exists('yellow_threshold', **kwargs), key_exists('count', **kwargs), 
                             key_exists('increment', **kwargs),key_exists('decrement', **kwargs), key_exists('oldname', **kwargs))) 
            
    result = club_exist(key_exists('name', **kwargs))
    if(len(result)==1):
        return 'information modified successfully'



def update_club_count(**kwargs):
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

    result = club_exist(key_exists('oldname', **kwargs))
    if(len(result)==0):
        result = key_exists('oldname', **kwargs) + ' doesnot exists'
        return result


    result = get_clubs_bouncer(key_exists('oldname', **kwargs))
    if(result != [(key_exists('bouncer_email', **kwargs),)]):
        result = key_exists('bouncer_email', **kwargs) + ' is not the bouncer of ' + key_exists('oldname', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('bouncer_email', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'bouncer needs to login to modify club details'
        return result

    result = exec_commit('''UPDATE clubs SET  name=%s, city =%s, music=%s, capacity = %s, yellow_threshold=%s,
                            current_count = %s, increment= %s, decrement =%s
                            WHERE name = %s ''', 
                            (key_exists('name', **kwargs), key_exists('city', **kwargs), key_exists('music', **kwargs),
                             key_exists('capacity', **kwargs), key_exists('yellow_threshold', **kwargs), key_exists('count', **kwargs), 
                             key_exists('increment', **kwargs),key_exists('decrement', **kwargs), key_exists('oldname', **kwargs))) 
            
    result = club_exist(key_exists('name', **kwargs))
    if(len(result)==1):
        return 'information modified successfully'





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

    result = exec_commit('''UPDATE users SET role=%s
                            where email in (select email from managers where club=%s)''', 
                            ('user',key_exists('club_name', **kwargs)))
    
    result = exec_commit('''UPDATE users SET role=%s
                            where email in (select email from bouncers where club=%s)''', 
                            ('user',key_exists('club_name', **kwargs)))

    result = exec_commit('''Delete from clubs where name = %s ''' 
                            , (key_exists('club_name', **kwargs),)) 

    
            
    result = club_exist(key_exists('club_name', **kwargs))
    if(len(result)==0):
        return "club is deleted successfully"
    


##########################################################
#------------------ Customer functions ----------------------
###########################################################

def current_club_customer(customer):
    result = exec_get_all(''' SELECT * 
                                FROM clubs
                                where name= (select club 
                                            from entered 
                                            where email=%s and left_time is null)''', (customer,)) 
    return result

##########################################################
#------------------ Entry functions ----------------------
###########################################################


def list_not_entered(**kwargs):


    result = exec_get_all(''' SELECT * 
                                FROM users
                                where role='user' ''') 
    return(result)

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

    result = club_exist(key_exists('club', **kwargs))
    if(len(result)==0):
        result = key_exists('club', **kwargs) + ' doesnot exists'
        return result

    result = user_exist(key_exists('bouncer_email', **kwargs))
    if(len(result)==0):
        result = key_exists('bouncer_email', **kwargs) + ' doesnot exists'
        return result

    result = get_bouncers_club(key_exists('bouncer_email', **kwargs))
    if(result[0][0] != key_exists('club', **kwargs)):
        result = key_exists('bouncer_email', **kwargs) + ' is not the bouncer of ' + key_exists('club', **kwargs)
        return result

    result = authenticate_seesion_id(key_exists('bouncer_email', **kwargs), key_exists('session_id', **kwargs))
    if(len(result)==0):
        result = 'bouncer needs to login to allow entry to club'
        return result

    result = get_entry(key_exists('club', **kwargs),key_exists('email', **kwargs)) 
    if (len(result)==1):
        return key_exists('email', **kwargs) + ' is already in the club'

    current_timestamp = datetime.now()
    # current_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    current_count = get_current_entries_in_club(key_exists('club', **kwargs),current_timestamp)
    capacity = get_club_capacity(key_exists('club', **kwargs))
    if (current_count[0][0]<capacity[0][0]):
        result = exec_commit('''INSERT INTO entered(email, club, enter_time, left_time, amount_spent) 
                                VALUES (%s,%s,%s,%s,%s)''', 
                                (key_exists('email', **kwargs), key_exists('club', **kwargs),
                                current_timestamp,key_exists('left_time', **kwargs), 
                                key_exists('amount_spent', **kwargs))) 

        result = exec_commit('''UPDATE users SET role=%s
                            where email=%s''', 
                            ('customer',key_exists('email', **kwargs)))

        result = get_current_entries_in_club(key_exists('club', **kwargs),current_timestamp )
        if(len(result) == current_count[0][0]+1):
            return "added customer successfully"
    else:
        return 'full capacity, cant enter'

def leave_club(**kwargs):
    """enter users to the club.
    
    access: Bouncers

    kewword arguments:
    club_name -- name of the club
    user_name -- name of the person adding the club
    amount_spent -- the amount person spent in the club
    left_time -- time at which person is leaving the club
    """

    result = club_exist(key_exists('club', **kwargs))
    if(len(result)==0):
        result = key_exists('club', **kwargs) + ' doesnot exists'
        return result

    entry = get_entry(key_exists('club', **kwargs), key_exists('email', **kwargs))
    if(len(entry)==0):
        result = key_exists('email', **kwargs) +' is not present in the club'
        return result

    current_timestamp = datetime.now()

    result = exec_commit('''UPDATE entered SET left_time=%s, amount_spent=%s 
                            Where id =%s''', 
                            (current_timestamp, key_exists('amount_spent', **kwargs),entry[0][0])) 

    result = exec_commit('''UPDATE users SET role=%s
                            where email=%s''', 
                            ('user',key_exists('email', **kwargs)))


    result = get_entry(key_exists('club', **kwargs), key_exists('email', **kwargs))
    if (len(result)==0):
        return 'removed customer susscessfully'

def get_entry(club, email):
    """return the record if user is preseent in the club.
    
    access: eveloper

    arguments:
    club_name -- name of the club
    user_name -- name of the person adding the club
    """
    result = exec_get_all('''SELECT *
                            FROM entered
                            WHERE email = %s and club= %s and left_time is null''', 
                            (email, club)) 

    return result

def current_entries_in_club(club):
    """return the record if user is preseent in the club.
    
    access: eveloper

    arguments:
    club_name -- name of the club
    user_name -- name of the person adding the club
    """
    # result = exec_get_all('''SELECT email enter_time
    #                         FROM entered
    #                         WHERE club= %s and left_time is null''', 
    #                         (club,)) 
    
    result = exec_get_all('''SELECT email, enter_time
                            FROM entered
                            where club = %s and left_time is null
                            ''', (club,)) 


    return result

def get_current_entries_in_club(club, enter_time):
    """return all the entries for a given date and club.
    
    access: eveloper

    arguments:
    club_name -- name of the club
    enter_time -- time of entry into the club
    """
    result = exec_get_all('''SELECT count(id)
                            FROM entered
                            WHERE club= %s and date(enter_time) = date(%s)''', 
                            (club,enter_time)) 
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


def filterClubsInfo(**kwargs):

    if (key_exists('date', **kwargs) == '' and key_exists('population', **kwargs) == '' and key_exists('earning', **kwargs) == ''):
        result = exec_get_all(''' 
                            SELECT *
                            FROM clubs
                            order by clubs.name  ''')
        return result
        
    if (key_exists('earning', **kwargs) == '' and key_exists('population', **kwargs) == ''):

        result = exec_get_all(''' 
                            SELECT *
                            FROM clubs
                            order by clubs.name  ''')
        return result

    if (key_exists('date', **kwargs) == '' and key_exists('population', **kwargs) == ''):

        result = exec_get_all('''SELECT *
                                 FROM clubs where name in (select club
                                FROM entered 
                                Group By club 
                                having SUM(amount_spent)>= %s)
                                order by clubs.name
                                ''',(key_exists('earning', **kwargs),)) 
        return result

    if (key_exists('date', **kwargs) == '' and key_exists('earning', **kwargs) == ''):
        result = exec_get_all('''SELECT *
                                FROM clubs where name in (select club
                                                    FROM entered 
                                                    Group By club 
                                                    having count(id) >=%s) 
                                                    order by clubs.name
                                                    ''',(key_exists('population', **kwargs),)) 
        return result

    if (key_exists('date', **kwargs) == '' ):
        result = exec_get_all('''SELECT *
                                FROM clubs where name in (select club
                                                FROM entered
                                                Group BY club
                                                having SUM(amount_spent)>=%s and count(id)>=%s) ''',
                                                (key_exists('earning', **kwargs),key_exists('population', **kwargs))) 
        return result

    if (key_exists('earning', **kwargs) == '' ):
        result = exec_get_all('''SELECT *
                                FROM clubs where name in (select club
                                                    FROM entered 
                                                    where date(enter_time) = date(%s)
                                                    Group By club 
                                                    having count(id) >=%s) 
                                                    order by clubs.name
                                                    ''',(key_exists('date', **kwargs),key_exists('population', **kwargs))) 
        return result

    if (key_exists('population', **kwargs) == '' ):
        result = exec_get_all('''SELECT *
                                FROM clubs where name in (select club
                                                    FROM entered 
                                                    where date(enter_time) = date(%s)
                                                    Group By club 
                                                    having SUM(amount_spent)>=%s)
                                                    order by clubs.name
                                                    ''',(key_exists('date', **kwargs),key_exists('earning', **kwargs))) 
        return result
    

    else:
        result = exec_get_all('''SELECT *
                                FROM clubs where name in (select club
                                                    FROM entered 
                                                    where date(enter_time) = date(%s)
                                                    Group By club 
                                                    having SUM(amount_spent)>= %s  and count(id) >=%s) 
                                                    order by clubs.name
                                                    ''',(key_exists('date', **kwargs),key_exists('earning', **kwargs), key_exists('population', **kwargs))) 
    
        return result





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



##########################################################
#--------------- Reservation functions -------------------
###########################################################

def list_reservaion(club):
    current_timestamp = datetime.now()
    result = exec_get_all('''select email, club
                             from reservations
                             where club=%s and date(date)=date(%s)''', (club,current_timestamp))
    return result



def insert_reservation(**kwargs):
    result = exec_get_all('''select *
                             from reservations
                             where email=%s and date=%s''', (key_exists('email', **kwargs),key_exists('date', **kwargs)))

    if(len(result)==0):
        result = exec_commit('''INSERT INTO reservations(email, club, date) 
                                VALUES (%s,%s,%s)''', 
                                (key_exists('email', **kwargs), key_exists('club', **kwargs),
                                key_exists('date', **kwargs)))
        result = exec_get_all('''select *
                             FROM reservations
                             where email=%s and date=%s''', (key_exists('email', **kwargs),key_exists('date', **kwargs)))
        if(len(result)==1):
            return 'reservation created'
    
    return 'only 1 reservaion per day'


def del_reservation(**kwargs):
    # print(key_exists('date', **kwargs))
    # print(key_exists('email', **kwargs))
    # print(key_exists('club', **kwargs))
    result = exec_get_all('''select *
                             from reservations
                             where email=%s and date=%s and club=%s''', 
                             (key_exists('email', **kwargs),key_exists('date', **kwargs),key_exists('club', **kwargs) ))

    if(len(result)==1):
        result = exec_commit('''Delete from reservations where email=%s and date=%s and club=%s''', 
                             (key_exists('email', **kwargs),key_exists('date', **kwargs),key_exists('club', **kwargs) ))

        result = exec_get_all('''select *
                             from reservations
                             where email=%s and date=%s and club=%s''', 
                             (key_exists('email', **kwargs),key_exists('date', **kwargs),key_exists('club', **kwargs) ))
        if(len(result)==0):
            return 'Reservation Deleted'
    
    return 'No Reservation Found'