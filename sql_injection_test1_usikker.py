from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# tilslutning til database
conn = mysql.connector.connect(
    host="sql7.freesqldatabase.com",
    user="sql7774910",
    password="R7kHhP7P8Z",
    database="sql7774910"
)

@app.route('/search')
def search():
    name = request.args.get('name')
    cursor = conn.cursor()
    query = f"SELECT * FROM customers WHERE email = '{name}'" # <-- sårbar query
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return {'results': results}

if __name__ == '__main__':
    app.run(debug=True)
    