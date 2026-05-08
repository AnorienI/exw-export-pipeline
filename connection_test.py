import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        # Standard XAMPP Linux defaults
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='', 
            database='exw_fca' 
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
        print(f"❌ Error: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔒 Connection closed.")

if __name__ == "__main__":
    test_connection()