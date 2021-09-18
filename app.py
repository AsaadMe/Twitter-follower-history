from flask import Flask, render_template
import follower_history

app = Flask(__name__)

@app.route('/')
def index():
    follower_history.db_set()
    users_history = follower_history.db_get()  # {username1: {"x-x-x":654, ...}, ...}
    
    users = []
    for name, vals in users_history.items():
        users.append({"name":name, "counts":list(vals.values())})
    
    dates = set()
    for user_values in users_history.values():
        for date in user_values.keys():
            dates.add(date)
    print(users)
    return render_template("graph.html", users=users, dates=list(dates))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)