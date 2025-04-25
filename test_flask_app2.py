from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Rollekort med tilladte kolonner pr. tabel
role_permissions = {
    "products": {
        "admin": "SELECT * FROM products",
        "analytics": "SELECT product_id, product_name, model_year, list_price FROM products"
    },
    "stocks": {
        "admin": "SELECT store_name, product_id, quantity FROM stocks",
        "analytics": "SELECT store_name, quantity FROM stocks"
    }
}

@app.route("/data")
def get_data():
    table = request.args.get("table")
    role = request.args.get("role")
    user = request.args.get("user")
    password = request.args.get("password")

    if not all([table, role, user, password]):
        return jsonify({"error": "Parametre 'table', 'role', 'user' og 'password' skal angives"}), 400

    if table not in role_permissions or role not in role_permissions[table]:
        return jsonify({"error": "Ugyldig rolle eller tabel"}), 403

    query = role_permissions[table][role]

    db_config = {
        "host": "localhost",
        "user": user,
        "password": password,
        "database": "new_bikecorp_db"
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
