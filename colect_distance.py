import requests
import pandas as pd

# 1. Definição das cidades para o estudo de caso
cidades_estudo = {
    "Raio Curto": ["Campinas", "Jundiaí", "Sorocaba"],
    "Raio Médio": ["Ribeirão Preto", "Bauru", "Piracicaba"],
    "Raio Longo": ["São José do Rio Preto", "Araçatuba", "Presidente Prudente"]
}

def get_city_data(city_name):
    # Consulta a API de Localidades do IBGE para o estado de SP (ID 35)
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/35/municipios"
    response = requests.get(url)
    
    if response.status_code == 200:
        municipios = response.json()
        for m in municipios:
            # Busca exata pelo nome (ignorando maiúsculas/minúsculas)
            if m['nome'].lower() == city_name.lower():
                return {
                    "id_ibge": m['id'],
                    "nome": m['nome'],
                    "microrregiao": m['microrregiao']['nome']
                }
    return None

def get_road_distance(lat1, lon1, lat2, lon2):
    # Coordenadas aproximadas do Porto de Santos (Cais)
    # Usando OSRM para distância rodoviária real em vez de linha reta
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        # Distância vem em metros, convertendo para km
        return round(data['routes'][0]['distance'] / 1000, 2)
    return None

# Coordenadas do Porto de Santos para o cálculo
SANTOS_COORDS = (-23.96, -46.33) 

print(f"{'Categoria':<15} | {'Cidade':<25} | {'ID IBGE':<10} | {'Dist. Santos (km)'}")
print("-" * 75)

for categoria, lista in cidades_estudo.items():
    for cidade in lista:
        info = get_city_data(cidade)
        if info:
            # Nota: Para coordenadas exatas via IBGE, usaríamos a API de Malhas
            # Aqui simularemos a lógica que você vai automatizar
            # (Valores de distância para validação manual)
            distancia = get_road_distance(-23.96, -46.33, -22.90, -47.06) # Exemplo Campinas
            print(f"{categoria:<15} | {info['nome']:<25} | {info['id_ibge']:<10} | Pendente consulta OSRM")