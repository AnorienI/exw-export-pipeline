import requests
import time

cidades_estudo = {
    "Raio Curto": ["Campinas", "Jundiaí", "Sorocaba"],
    "Raio Médio": ["Ribeirão Preto", "Bauru", "Piracicaba"],
    "Raio Longo": ["São José do Rio Preto", "Araçatuba", "Presidente Prudente"]
}

# Coordenadas do Porto de Santos (Cais)
SANTOS_LAT, SANTOS_LON = -23.96, -46.33

def get_coords_and_dist(city_name):
    # 1. Busca coordenadas via API de Localidades (IBGE)
    # Nota: A API de localidades não dá lat/lon direto, 
    # usamos o buscador do OpenStreetMap (Nominatim) que é gratuito
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city_name}&state=Sao+Paulo&format=json"
    headers = {'User-Agent': 'exw-fca-pipeline-study'}
    
    try:
        geo_res = requests.get(geo_url, headers=headers).json()
        if not geo_res: return None
        
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']
        
        # 2. Busca distância rodoviária via OSRM
        osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lon},{lat};{SANTOS_LON},{SANTOS_LAT}?overview=false"
        route_res = requests.get(osrm_url).json()
        
        dist_km = round(route_res['routes'][0]['distance'] / 1000, 2)
        return dist_km
    except Exception as e:
        return f"Erro: {e}"

print(f"{'Categoria':<15} | {'Cidade':<25} | {'Dist. Santos (km)'}")
print("-" * 65)

for categoria, lista in cidades_estudo.items():
    for cidade in lista:
        distancia = get_coords_and_dist(cidade)
        print(f"{categoria:<15} | {cidade:<25} | {distancia} km")
        time.sleep(1) # Pausa amigável para as APIs gratuitas