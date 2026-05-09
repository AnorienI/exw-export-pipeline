import os
import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        # Load environment variables from .env
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
        DB_PORT = os.getenv('DB_PORT', 3306)
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_DATABASE = os.getenv('DB_DATABASE', 'exw_fca')

        # Standard XAMPP Linux defaults
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Success! Connected to MariaDB version: {db_info}")

            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            print("\n📂 Tables found in your database:")
            for table in tables:
                print(f" - {table[0]}")

    except Error as e:
        # Log the error for easier debugging
        import logging
        logging.error(f"❌ Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔒 Connection closed.")

if __name__ == "__main__":
    test_connection()

