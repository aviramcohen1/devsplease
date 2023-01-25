from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/data')
def data():
    con = psycopg2.connect(
        host="hostname",
        port="portnumber",
        database="dbname",
        user="username",
        password="password"
    )
    cur = con.cursor()
    print("00")
    print(cur)
    print("000")
    cur.execute("SELECT * FROM users_git_from_israel")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
