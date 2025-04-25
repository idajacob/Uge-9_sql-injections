from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/union-test")
def union_test():
    name = request.args.get("name")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",  # skift evt bruger
            password="adminpass",
            database="new_bikecorp_db"
        )
        cursor = conn.cursor()

        # Sårbar SQL (uden parameterisering)
        query = f"SELECT product_name FROM products WHERE product_name = '{name}'"
        print("Kører query:", query)
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
