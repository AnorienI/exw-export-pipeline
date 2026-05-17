import requests
import mysql.connector
from common import get_coords_and_dist

# Geolocation coordinates (Latitude, Longitude)
ORIGIN_COORDS = "-21.1775,-47.8103"
SANTOS_PORT_COORDS = "-23.9618,-46.3022"

# ANTT / Market Freight rate parameter: cost per KM per ton (in BRL)
FREIGHT_RATE_PER_KM_TON = 2.50
CARGO_WEIGHT_TONS = 12.0

def calculate_inland_freight(city_name):
    distance_km = get_coords_and_dist(city_name)
    
    if isinstance(distance_km, str):
        print(distance_km)
        return
    
    total_freight_brl = distance_km * FREIGHT_RATE_PER_KM_TON * CARGO_WEIGHT_TONS
    
    print(f"🛣️ Distance to Santos: {distance_km:.2f} KM")
    print(f"🚚 Estimated Inland Freight: R$ {total_freight_brl:.2f}")

    # Save directly to your MariaDB logistics_fees table
    conn = mysql.connector.connect(host='127.0.0.1', user='root', database='exw_fca')
    cursor = conn.cursor()
    
    sql = """INSERT INTO logistics_fees (route_name, distance_km, total_cost_brl) 
             VALUES ('{city_name}_to_Santos', %s, %s)
             ON DUPLICATE KEY UPDATE distance_km = VALUES(distance_km), total_cost_brl = VALUES(total_cost_brl)"""
    
    cursor.execute(sql, (distance_km, total_freight_brl))
    conn.commit()
    print("💾 Logistics database updated successfully.")

if __name__ == "__main__":
    cities_estudo = {
        "Raio Curto": ["Campinas", "Jundiaí", "Sorocaba"],
        "Raio Médio": ["Ribeirão Preto", "Bauru", "Piracicaba"],
        "Raio Longo": ["São José do Rio Preto", "Araçatuba", "Presidente Prudente"]
    }
    
    for categoria, lista in cities_estudo.items():
        for cidade in lista:
            calculate_inland_freight(cidade)

