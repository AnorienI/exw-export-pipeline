import requests
import mysql.connector

# Geolocation coordinates (Latitude, Longitude)
# Example: From a farm in Ribeirão Preto to the Port of Santos
ORIGIN_COORDS = "-21.1775,-47.8103"      
SANTOS_PORT_COORDS = "-23.9618,-46.3022" 

# ANTT / Market Freight rate parameter: cost per KM per ton (in BRL)
# Adjust this variable based on realistic market diesel/freight updates
FREIGHT_RATE_PER_KM_TON = 2.50  
CARGO_WEIGHT_TONS = 12.0  # e.g., a standard truckload of honey boxes

def calculate_inland_freight():
    try:
        # 1. Query the OpenStreetMap OSRM API for driving distance
        url = f"http://router.project-osrm.org/route/v1/driving/{ORIGIN_COORDS};{SANTOS_PORT_COORDS}?overview=false"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['code'] != 'Ok':
            raise Exception("OSRM API routing failed.")
            
        # OSRM returns distance in meters; convert to kilometers
        distance_kms = data['routes'][0]['distance'] / 1000.0
        
        # 2. Compute total road transport cost
        total_freight_brl = distance_kms * FREIGHT_RATE_PER_KM_TON * CARGO_WEIGHT_TONS
        
        print(f"🛣️ Distance to Santos: {distance_kms:.2f} KM")
        print(f"🚚 Estimated Inland Freight: R$ {total_freight_brl:.2f}")

        # 3. Save directly to your MariaDB logistics_fees table
        conn = mysql.connector.connect(host='127.0.0.1', user='root', database='exw_fca')
        cursor = conn.cursor()
        
        sql = """INSERT INTO logistics_fees (route_name, distance_km, total_cost_brl) 
                 VALUES ('Rib_Preto_to_Santos', %s, %s)
                 ON DUPLICATE KEY UPDATE distance_km = VALUES(distance_km), total_cost_brl = VALUES(total_cost_brl)"""
        
        cursor.execute(sql, (distance_kms, total_freight_brl))
        conn.commit()
        print("💾 Logistics database updated successfully.")

    except Exception as e:
        print(f"❌ Logistics Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    calculate_inland_freight()
