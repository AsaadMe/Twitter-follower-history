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
    
def db_set():
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

def db_set_test():
    dbase = redis.Redis(host='db', port=6379)
    users = get_users()
    next_date = '2021-9-20'
    next2_date = '2021-9-21'
    for user in users:
        count = follower_counter(user)
        out_val = {}
        if (val := dbase.get(user)) != None:
            out_val = json.loads(val)
        out_val.update({next_date:count+330})
        dbase.set(user, json.dumps(out_val))
        
        out_val.update({next2_date:count-110})
        dbase.set(user, json.dumps(out_val))
    
def db_get():
    dbase = redis.Redis(host='db', port=6379)
    users = get_users()
    return {user:json.loads(dbase.get(user)) for user in users}