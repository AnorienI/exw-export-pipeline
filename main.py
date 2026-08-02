import os
import sys
import getpass
import mysql.connector
from dotenv import load_dotenv
import unicodedata

def normalizar_texto(texto):
    """Remove acentos e converte para minúsculas."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()

load_dotenv()

def get_db_connection():
    db_user = os.getenv("DB_USER", "anorien")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", 3306))
    db_name = os.getenv("DB_NAME", "exw_fca")

    # Se a senha não estiver no arquivo .env, pede no terminal
    if not db_password:
        db_password = getpass.getpass(prompt=f"Digite a senha do MariaDB para o usuário '{db_user}': ")

    try:
        conn = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
        return conn
    except mysql.connector.Error as e:
        print(f"\n[ERRO] Falha na conexão com o MariaDB: {e}")
        sys.exit(1)

def obter_ou_criar_origem(conn, cursor, nome_cidade):
    """Busca a origem no banco ou cadastra se não existir."""
    cursor.execute("SELECT origin_id FROM origins WHERE city = %s", (nome_cidade,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    cursor.execute(
        "INSERT INTO origins (name, city, state, country) VALUES (%s, %s, %s, %s)",
        (f"Origem {nome_cidade}", nome_cidade, "SP", "BR")
    )
    conn.commit()
    return cursor.lastrowid

def obter_ou_criar_produto(conn, cursor, nome_produto, preco_exw):
    """Busca o produto ou insere um novo com o preço EXW base."""
    cursor.execute("SELECT product_id FROM products WHERE name = %s", (nome_produto,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    cursor.execute(
        "INSERT INTO products (name, hs_code, unit_weight_kg, price_exw_brl) VALUES (%s, %s, %s, %s)",
        (nome_produto, "1701.14.00", 1000.00, preco_exw)
    )
    conn.commit()
    return cursor.lastrowid

def estimar_distancia_santos(cidade_origem):
    """Retorna a distância aproximada para o Porto de Santos."""
    distancias_conhecidas = {
        "São José do Rio Preto": 498.0,
        "Campinas": 180.0,
        "Ribeirão Preto": 415.0
    }
    return distancias_conhecidas.get(cidade_origem, 450.0)

def calcular_frete_por_produto(distancia_km, nome_produto):
    """Calcula o frete com base na distância e no tipo de carga."""
    taxa_base_km_ton = 0.26  # R$ por km/tonelada
    
    multiplicador = 1.0
    if "Açúcar" in nome_produto or "Sugarcane" in nome_produto:
        multiplicador = 1.08  # Carga a granel / logística dedicada
    elif "Café" in nome_produto:
        multiplicador = 1.05
        
    return round(distancia_km * taxa_base_km_ton * multiplicador, 2)

def main():
    print("\n==================================================")
    print("   EXW to FCA Pipeline - Calculador Integrado    ")
    print("==================================================")

    # Conecta ao banco (pedindo a senha se necessário)
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Prompts interativos
        cidade_origem = input("\n[1/3] Digite a cidade de origem (ex: São José do Rio Preto): ").strip()
        if not cidade_origem:
            cidade_origem = "São José do Rio Preto"

        nome_produto = input("[2/3] Digite o nome do produto (ex: Açúcar VHP): ").strip()
        if not nome_produto:
            nome_produto = "Açúcar VHP"

        preco_input = input("[3/3] Digite o preço EXW por tonelada em R$ (ex: 2500): ").strip()
        preco_exw = float(preco_input) if preco_input else 2500.00

        # Persistência e Recuperação de IDs
        origin_id = obter_ou_criar_origem(conn, cursor, cidade_origem)
        product_id = obter_ou_criar_produto(conn, cursor, nome_produto, preco_exw)
        port_id = 1  # Porto de Santos (BRSSZ)

        # Cálculo da Logística
        distancia_km = estimar_distancia_santos(cidade_origem)
        custo_frete_ton = calcular_frete_por_produto(distancia_km, nome_produto)

        # Atualização/Inserção na freight_matrix
        cursor.execute("""
            INSERT INTO freight_matrix (origin_id, port_id, cost_per_ton, distance_km)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE cost_per_ton = VALUES(cost_per_ton), distance_km = VALUES(distance_km)
        """, (origin_id, port_id, custo_frete_ton, int(distancia_km)))

        conn.commit()

        # Cálculo Final
        preco_fca_estimado = preco_exw + custo_frete_ton

        # Exibição do Relatório
        print("\n==================================================")
        print("               RESUMO DO PIPELINE                 ")
        print("==================================================")
        print(f" Cidade Origem:   {cidade_origem}")
        print(f" Porto Destino:   Porto de Santos (BRSSZ)")
        print(f" Produto:         {nome_produto}")
        print(f" Distância:       {distancia_km} km")
        print(f" Frete Estimado:  R$ {custo_frete_ton:.2f} / ton")
        print("--------------------------------------------------")
        print(f" Preço EXW:       R$ {preco_exw:.2f} / ton")
        print(f" Preço FCA Santos:R$ {preco_fca_estimado:.2f} / ton")
        print("==================================================\n")

    except Exception as e:
        print(f"\n[ERRO] Falha na execução: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()