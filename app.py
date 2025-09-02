from flask import Flask, request, redirect
import jwt
import time
import json
import os
from google.oauth2 import service_account

app = Flask(__name__)

# Leer las credenciales desde la variable de entorno
service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Extraer email y private key directamente del JSON
SERVICE_ACCOUNT_EMAIL = service_account_info["client_email"]
PRIVATE_KEY = service_account_info["private_key"]

ISSUER_ID = "3388000000022978257"
CLASS_ID = "itm-group-directorio"

@app.route("/google-pass")
def google_pass():
    persona = request.args.get("persona", "demo")

    object_id = f"{ISSUER_ID}.obj-{persona}"

    # Objeto genérico
    generic_object = {
    "id": object_id,
    "classId": f"{ISSUER_ID}.{CLASS_ID}",
    "state": "ACTIVE",
    "accountId": persona,
    "accountName": f"Contacto {persona}",
    "barcode": {
        "type": "QR_CODE",
        "value": f"https://itmgroup.mx/directorio/{persona}/",
        "alternateText": persona
    },
    "heroImage": {
        "sourceUri": {
            "uri": "https://itmgroup.mx/core/views/ed294a0d7e/assets/logo-ITM-Group.png"
        },
        "contentDescription": {
            "defaultValue": {
                "language": "es",
                "value": "Logo ITM Group"
            }
        }
    },
    "cardTitle": {
        "defaultValue": {
            "language": "es",
            "value": "Directorio ITM"
        }
    },
    "header": {
        "defaultValue": {
            "language": "es",
            "value": "Directorio ITM"
        }
    },
    "textModulesData": [
        {
            "header": "Directorio-ITM",
            "body": "Directorio-Directores-ITM"
        }
    ]
}

    # Construir JWT
    jwt_payload = {
        "iss": SERVICE_ACCOUNT_EMAIL,
        "aud": "google",
        "typ": "savetowallet",
        "iat": int(time.time()),
        "payload": {
            "genericObjects": [generic_object]
        }
    }

    token = jwt.encode(jwt_payload, PRIVATE_KEY, algorithm="RS256")

    # URL final para Save to Wallet
    save_url = f"https://pay.google.com/gp/v/save/{token}"

    return redirect(save_url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
