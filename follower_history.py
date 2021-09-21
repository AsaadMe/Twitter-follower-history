from database_com import *

import datetime
import json

import redis
import requests

def follower_counter(username):
    
    link = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names="

    # return requests.get(link+username).json()[0]["followers_count"]
    outs = {"tparsi":120, "ammir":230, "hamzeghalebi":490, "azodiac83":123, "h0d3r_fa":450, 
            "GhoreishiG":390, "solmazazhdari":256, "farnazfassihi":765, "negarmortazavi":670}
    return outs[username]

def get_users():
    with open("accounts.txt", "r") as file:
        return file.read().splitlines()
    
def redis_set():
    dbase = redis.Redis(host='db', port=6379)
    users = get_users()
    today_date = str(datetime.date.today())
    for user in users:
        count = follower_counter(user)
        out_val = {}
        if (val := dbase.get(user)) != None:
            out_val = json.loads(val)
        out_val.update({today_date:count})
        dbase.set(user, json.dumps(out_val))

def redis_set_test():
    dbase = redis.Redis(host='db', port=6379)
    users = get_users()
    next_date = '2021-09-20'
    next2_date = '2021-09-21'
    for user in users:
        count = follower_counter(user)
        out_val = {}
        if (val := dbase.get(user)) != None:
            out_val = json.loads(val)
        out_val.update({next_date:count+330})
        dbase.set(user, json.dumps(out_val))
        
        out_val.update({next2_date:count-110})
        dbase.set(user, json.dumps(out_val))
    
def redis_get():
    dbase = redis.Redis(host='db', port=6379)
    users = get_users()
    return {user:json.loads(dbase.get(user)) for user in users}


def pg_set():
    connection = create_connection(
    "fol-tw", "usr", "secret", "db", "5432")
    create_table(connection)
    insert_query = "INSERT INTO users (name, count, date) VALUES (%s, %s, %s)"
    user_names = get_users()
    today_date = str(datetime.date.today())
    for user in user_names:
        count = follower_counter(user)
        get_q = "SELECT date FROM users WHERE date=%s AND name=%s"
        user_date = execute_read_query(connection, get_q, today_date, user)
        if len(user_date) == 0:
            insert_exec(connection, insert_query, (user, count, today_date))
    
def pg_set_test():
    connection = create_connection(
    "fol-tw", "usr", "secret", "db", "5432")
    insert_query = "INSERT INTO users (name, count, date) VALUES (%s, %s, %s)"
    user_names = get_users()
    next_date = '2021-09-23'
    next2_date = '2021-09-25'
    for user in user_names:
        count = follower_counter(user)
        get_q = "SELECT date FROM users WHERE (date=%s OR date=%s) AND name=%s"
        user_date = execute_read_query(connection, get_q, next_date, next2_date, user)
        if len(user_date) == 0:
            insert_exec(connection, insert_query, (user, count+320, next_date))
            insert_exec(connection, insert_query, (user, count-120, next2_date))
            
           
def pg_get():
    connection = create_connection(
    "fol-tw", "usr", "secret", "db", "5432")
    out = {}
    for user_name in get_users():
        select_users = "SELECT * FROM users WHERE name=%s"
        user_data = execute_read_query(connection, select_users, user_name)
        out[user_name] = {date:count for (_, _, count, date) in user_data}
    return out