from flask import Flask, request, redirect
import jwt
import time
import json

app = Flask(__name__)

# Cargar credenciales de la service account
with open("service-account.json", "r") as f:
    creds = json.load(f)

SERVICE_ACCOUNT_EMAIL = creds["client_email"]
PRIVATE_KEY = creds["private_key"]
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
