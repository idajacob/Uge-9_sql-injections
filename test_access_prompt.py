import mysql.connector
from mysql.connector import Error
import getpass
from datetime import datetime

# Logfunktion – skriver til access_logs-tabellen
def log_access(cursor, username, action, status, table):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """
        INSERT INTO access_logs (log_time, username, action, status, target_table)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (timestamp, username, action, status, table))

# Input fra bruger
user = input("User name: ")
password = getpass.getpass("Passwords: ")

try:
    conn = mysql.connector.connect(
        host='localhost',
        user=user,
        password=password,
        database='new_bikecorp_db'
    )
    cursor = conn.cursor()

    # Test 1: SELECT på products
    action1 = "SELECT FROM products"
    print("\nPrøver SELECT på 'products'...")
    try:
        cursor.execute("SELECT product_name FROM products LIMIT 5;")
        for row in cursor.fetchall():
            print("OK -", row)
        log_access(cursor, user, action1, "SUCCESS", "products")
    except Error as e:
        print("Fejl i SELECT:", e)
        log_access(cursor, user, action1, "DENIED", "products")

    # Test 2: INSERT i products
    action2 = "INSERT INTO products"
    print("\nPrøver INSERT i 'products'...")
    insert_query = """
    INSERT INTO products (product_id, product_name, brand_id, category_id, model_year, list_price)
    VALUES (9999, 'LOGTEST DB', 1, 1, 2025, 999.99);
    """
    try:
        cursor.execute(insert_query)
        conn.commit()
        print("INSERT lykkedes ✅")
        log_access(cursor, user, action2, "SUCCESS", "products")
    except Error as e:
        print("Fejl ❌:", e)
        log_access(cursor, user, action2, "DENIED", "products")

    conn.commit()

except Error as e:
    print("Fejl ved forbindelse:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
