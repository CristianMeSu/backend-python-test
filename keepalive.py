import time
import random
import requests
from datetime import datetime

URL = "https://backend-python-test.onrender.com/"

def ping():
    try:
        requests.get(URL, timeout=10)
        print(f"{datetime.now()}: Ping enviado correctamente")
    except Exception as e:
        print(f"{datetime.now()}: Error en el ping:", e)

if __name__ == "__main__":
    while True:
        ping()
        wait_minutes = random.randint(20, 27)
        print(f"Esperando {wait_minutes} minutos...")
        time.sleep(wait_minutes * 60)
