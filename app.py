from flask import Flask, request, redirect, send_file
from google.oauth2 import service_account
from flask import Flask, send_file, request
import jwt, time, json, os
from google.oauth2 import service_account
from py_pkpass.models import Pass, Barcode, BarcodeFormat, StoreCard

app = Flask(__name__)

# ==========================
# GOOGLE WALLET CONFIG
# ==========================
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
    nombre = request.args.get("nombre", "Usuario Demo")
    cargo = request.args.get("cargo", "Cargo Demo")

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
        "alternateText": cargo
    },
    "heroImage": {
        "sourceUri": {
            "uri": "https://itmgroup.mx/core/views/ed294a0d7e/assets/logo-ITM-Group-Blanco.png"
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
            "value": "ITM Group"
        }
    },
    "header": {
        "defaultValue": {
            "language": "es",
            "value": nombre
        }
    },
    "textModulesData": [
        {
            "header": "Directorio-ITM",
            "body": nombre
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

# ==========================
# APPLE WALLET CONFIG
# ==========================
# Apple Wallet config
PASS_TYPE_IDENTIFIER = "pass.com.itmgroup.directorio"
TEAM_IDENTIFIER = "TU_TEAM_ID"
CERT_P12_PATH = os.path.join("/etc/secrets", "certificate.p12")
WWDR_PEM_PATH = os.path.join("/etc/secrets", "wwdr.pem")
CERT_P12_PASSWORD = os.environ.get("APPLE_P12_PASSWORD")

@app.route("/apple-pass")
def apple_pass():
    persona = request.args.get("persona", "demo")
    nombre = request.args.get("nombre", "Usuario Demo")
    cargo = request.args.get("cargo", "Cargo Demo")

    # Crear StoreCard (generic)
    card = StoreCard()
    card.addPrimaryField("nombre", nombre, "Nombre")
    card.addSecondaryField("cargo", cargo, "Cargo")

    passfile = Pass(
        card,
        passTypeIdentifier=PASS_TYPE_IDENTIFIER,
        organizationName="ITM Group",
        teamIdentifier=TEAM_IDENTIFIER
    )
    passfile.serialNumber = persona
    passfile.description = "Directorio ITM"

    passfile.barcode = Barcode(
    message=f"https://itmgroup.mx/directorio/{persona}/",
    format="PKBarcodeFormatQR",
    altText=cargo
    )

    # Añadir imágenes si las tienes disponibles
    # passfile.addFile("icon.png", open("icon.png", "rb"))
    passfile.addFile("icon.png", open("/etc/secrets/logo-ITM-Group-Blanco.png", "rb"))
    passfile.addFile("logo.png", open("/etc/secrets/logo-ITM-Group-Blanco.png", "rb"))

    # Generar archivo .pkpass
    filename = f"{persona}.pkpass"
    passfile.create(
        certificate=CERT_P12_PATH,
        key=CERT_P12_PATH,      # usar el mismo .p12 aquí
        wwdr_certificate=WWDR_PEM_PATH,
        password=CERT_P12_PASSWORD,
        output=filename
    )
    from flask import after_this_request
    import os

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            print(f"No se pudo borrar {filename}: {e}")
        return response
    
    return send_file(filename, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
