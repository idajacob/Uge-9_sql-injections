from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database config
db_config = {
    "host": "localhost",
    "user": "admin",  # eller en anden med adgang
    "password": "adminpass",
    "database": "new_bikecorp_db"
}

@app.route("/products")
def products():
    role = request.args.get("role")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if role == "admin":
            cursor.execute("SELECT * FROM products")
        elif role == "analytics":
            cursor.execute("SELECT product_id, product_name, model_year, list_price FROM products")
        else:
            return jsonify({"error": "Ugyldig rolle"}), 403

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
