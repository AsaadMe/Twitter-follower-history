from flask import Flask, render_template
import follower_history

app = Flask(__name__)

@app.route('/')
def index():
    users_history = follower_history.db_set_get()  # {username: follower num.}
    
    users = [username for username in users_history.keys()]
    counts = [int(count) for count in users_history.values()]
    
    return render_template("graph.html", users=users, counts=counts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)