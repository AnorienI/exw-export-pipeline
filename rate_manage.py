import requests
import mysql.connector
from datetime import datetime

# 1. The Mapping (Your "Gutenberg" Logic)
CURRENCIES = {
    'USD': '1',
    'EUR': '21619',
    'CNY': '21611'
}

def fetch_and_save_rates():
    try:
        # Connect to your XAMPP database
        conn = mysql.connector.connect(host='127.0.0.1', user='root', database='exw_fca')
        cursor = conn.cursor()

        for code, sgs_id in CURRENCIES.items():
            # BCB API URL for the last 1 value of the specific series
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{sgs_id}/dados/ultimos/1?formato=json"
            
            response = requests.get(url)
            data = response.json()
            
            rate_val = float(data[0]['valor'].replace(',', '.'))
            date_val = datetime.strptime(data[0]['data'], '%d/%m/%Y').date()

            # The "Safe" Insert (ON DUPLICATE KEY ensures we don't double-entry today's rate)
            sql = """INSERT INTO exchange_rates (currency_code, rate_to_brl, effective_date) 
                     VALUES (%s, %s, %s)
                     ON DUPLICATE KEY UPDATE rate_to_brl = VALUES(rate_to_brl)"""
            
            cursor.execute(sql, (code, rate_val, date_val))
            print(f"✅ {code}: R$ {rate_val} (Ref: {date_val})")

        conn.commit()
    except Exception as e:
        print(f"❌ Error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fetch_and_save_rates()