import time
import random
import requests
from datetime import datetime
import os

# URL a "pingear"
URL = "https://backend-python-test.onrender.com/"

# Ignorar cualquier proxy
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

def ping():
    try:
        # requests sin usar proxy
        requests.get(URL, timeout=10, proxies={})
        print(f"{datetime.now()}: Ping enviado correctamente")
    except Exception as e:
        print(f"{datetime.now()}: Error en el ping:", e)

if __name__ == "__main__":
    while True:
        ping()
        wait_minutes = random.randint(17, 22)
        print(f"Esperando {wait_minutes} minutos...")
        time.sleep(wait_minutes * 60)
