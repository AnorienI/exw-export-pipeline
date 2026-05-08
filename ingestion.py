import mysql.connector

def ingest_freight_data():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='exw_fca'
        )
        cursor = connection.cursor()

        # Route data: (origin_id, port_id, distance_km, cost_per_ton)
        # 1: Varginha (MG) -> Santos (SP)
        # 2: Cascavel (PR) -> Paranaguá (PR)
        routes = [
            (1, 1, 450, 185.50), 
            (2, 2, 630, 210.00)
        ]

        sql = """INSERT INTO freight_matrix (origin_id, port_id, distance_km, cost_per_ton) 
                 VALUES (%s, %s, %s, %s)
                 ON DUPLICATE KEY UPDATE 
                 distance_km=VALUES(distance_km), 
                 cost_per_ton=VALUES(cost_per_ton)"""

        cursor.executemany(sql, routes)
        connection.commit()
        
        print(f"✅ Successfully ingested {cursor.rowcount} freight routes.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    ingest_freight_data()