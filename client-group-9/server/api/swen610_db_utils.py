import psycopg2
import psycopg2.extras
import yaml
import os
import pandas as pd
import hashlib
import secrets
import psycopg2
import yaml
import os

def connect():
    config = {}
    yml_path = os.path.join(os.path.dirname(__file__), '../../config/db.yml')
    with open(yml_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return psycopg2.connect(dbname=config['database'],
                            user=config['user'],
                            password=config['password'],
                            host=config['host'],
                            port=config['port'])

def exec_sql_file(path):
    full_path = os.path.join(os.path.dirname(__file__), f'{path}')
    conn = connect()
    cur = conn.cursor()
    with open(full_path, 'r') as file:
        cur.execute(file.read())
    conn.commit()
    conn.close()

def exec_get_one(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    one = cur.fetchone()
    conn.close()
    return one

def exec_get_all(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    # https://www.psycopg.org/docs/cursor.html#cursor.fetchall

    list_of_tuples = cur.fetchall()
    conn.close()
    return list_of_tuples

def exec_commit(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    conn.commit()
    conn.close()
    return result

def key_exists(key, **kwargs):
    """return the value for the given key if exist in the **kwargs.
    
    argmuments
    key -- key to be searched
    **kwargs -- keword arguments
    """
    if key in kwargs:
        return kwargs[key]
    else:
        return 

def insert_data_from_df(dataframe, table):
    """insert data in table in database from dataframe and return none if successful.
    
    argmuments
    dataframe -- pandas dataframe
    table -- nam eof table in database
    """
    conn = connect()
    cur = conn.cursor()

    tuples = [tuple(x) for x in dataframe.to_numpy()]
    columns = ','.join(list(dataframe.columns))
    sql = "INSERT INTO %s(%s) VALUES %%s" % (table, columns)
    psycopg2.extras.execute_values(cur, sql, tuples)
    conn.commit()
    conn.close()


def sha512(input_text):
    """converts the input text to hash digest using sha512.
    
    argmuments
    input_text -- the text for which hash is to be created. 
    """
    output_hash = hashlib.sha512()
    output_hash.update(input_text.encode('ASCII'))
    return output_hash.hexdigest()
     
def session_id_gen(max_value):
    """return a random integer in the given range.
    
    argmuments
    max_value -- range of the random number (0, max_value) 
    """
    return secrets.randbelow(max_value)
