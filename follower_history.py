import redis
import requests

def follower_counter(username):
    
    link = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names="

    return requests.get(link+username).json()[0]["followers_count"]

def db_set_get():
    dbase = redis.Redis(host='db', port=6379)
    
    users = ['twitter', 'joebiden']
    
    for user in users:
        count = follower_counter(user)
        dbase.set(user, count)
 
    return {user:dbase.get(user) for user in users}