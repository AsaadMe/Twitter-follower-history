import datetime

from flask import Flask, render_template, request, redirect, url_for
import follower_history

app = Flask(__name__)

def read_data():
    follower_history.pg_set()    
    users_history = follower_history.pg_get()  # {username1: {"x-x-x":654, ...}, ...}
    
    users = []
    for name, vals in users_history.items():
        users.append({"name":name, "counts":list(vals.values())})
    
    dates = set()
    for user_values in users_history.values():
        for date in user_values.keys():
            dates.add(date)
    
    dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in dates]
    dates.sort()
    sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    return users, sorteddates

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        follower_history.pg_set_test()
        return redirect(url_for("index"))
    else:     
        users, dates = read_data()
        return render_template("graph.html", users=users, dates=dates)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)