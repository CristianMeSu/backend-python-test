from flask import Flask, request, redirect, send_file, after_this_request
from google.oauth2 import service_account
from py_pkpass.models import Pass, Barcode, StoreCard
import jwt, time, json, os

app = Flask(__name__)

# ==========================
# GOOGLE WALLET CONFIG
# ==========================

#For localhost:
# Cargar credenciales de la service account
# with open("service-account.json", "r") as f:
#     creds = json.load(f)
# SERVICE_ACCOUNT_EMAIL = creds["client_email"]
# PRIVATE_KEY = creds["private_key"]

#For Production:
# Leer las credenciales desde la variable de entorno
service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(service_account_info)
SERVICE_ACCOUNT_EMAIL = service_account_info["client_email"]
PRIVATE_KEY = service_account_info["private_key"]

ISSUER_ID = "3388000000022978257"
CLASS_ID = "itm-group-directorio"

@app.route("/google-pass")
def google_pass():
    persona = request.args.get("persona", "demo")
    nombre = request.args.get("nombre", "Usuario Demo")
    cargo = request.args.get("cargo", "Cargo Demo")
    realestate = request.args.get("realestate", "false").lower() == "true"

    # =======================
    # Lógica según realestate
    # =======================
    if realestate:
        qr_url = f"https://itmdesarrolladores.com/directorio/{persona}/"
        hero_image = "https://www.itmdesarrolladores.com/core/views/547ab1bd38/assets/itm-logo.png"
        card_title = "ITM Desarrolladores"
        object_id = f"{ISSUER_ID}.obj-realestate-{persona}"
    else:
        qr_url = f"https://itmgroup.mx/directorio/{persona}/"
        hero_image = "https://itmgroup.mx/core/views/ed294a0d7e/assets/logo-ITM-Group-Blanco.png"
        card_title = "ITM Group"
        object_id = f"{ISSUER_ID}.obj-itm-{persona}"


    # Objeto genérico
    generic_object = {
        "id": object_id,
        "classId": f"{ISSUER_ID}.{CLASS_ID}",
        "state": "ACTIVE",
        "accountId": persona,
        "accountName": f"Contacto {persona}",
        "barcode": {
            "type": "QR_CODE",
            "value": qr_url,
            "alternateText": cargo
        },
        "heroImage": {
            "sourceUri": {"uri": hero_image},
            "contentDescription": {"defaultValue": {"language": "es", "value": "Logo"}}
        },
        "cardTitle": {"defaultValue": {"language": "es", "value": card_title}},
        "header": {"defaultValue": {"language": "es", "value": nombre}},
        "textModulesData": [{"header": "Directorio", "body": nombre}]
    }

    # Construir JWT
    jwt_payload = {
        "iss": SERVICE_ACCOUNT_EMAIL,
        "aud": "google",
        "typ": "savetowallet",
        "iat": int(time.time()),
        "payload": {"genericObjects": [generic_object]}
    }

    token = jwt.encode(jwt_payload, PRIVATE_KEY, algorithm="RS256")
    save_url = f"https://pay.google.com/gp/v/save/{token}"

    return redirect(save_url)

# ==========================
# APPLE WALLET CONFIG
# ==========================

PASS_TYPE_IDENTIFIER = "pass.itm-group-directorio"
TEAM_IDENTIFIER = "2ULQN9G3B2"
#For Localhost
# CERT_P12_PATH = os.path.join(".", "certificates", "certificate.p12")
# WWDR_PEM_PATH = os.path.join(".", "certificates", "wwdr.pem")

# For Production
# CERT_P12_PATH = os.path.join("/etc/secrets", "certificate.p12")
# WWDR_PEM_PATH = os.path.join("/etc/secrets", "wwdr.pem")
# CERT_P12_PASSWORD = os.environ.get("APPLE_P12_PASSWORD")

@app.route("/apple-pass")
def apple_pass():
    persona = request.args.get("persona")
    nombre = request.args.get("nombre")
    cargo = request.args.get("cargo")
    realestate = request.args.get("realestate", "false").lower() == "true"

    # =======================
    # Lógica según realestate
    # =======================
    if realestate:
        qr_url = f"https://itmdesarrolladores.com/directorio/{persona}/"
        ORG_NAME = "ITM Desarrolladores"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICON_PATH = os.path.join(BASE_DIR, "static", "realestate", "icon.png")
        LOGO_PATH = os.path.join(BASE_DIR, "static", "realestate", "logo.png")
        LOGO_2X_PATH = os.path.join(BASE_DIR, "static", "realestate", "logo@2x.png")
        LOGO_3X_PATH = os.path.join(BASE_DIR, "static", "realestate", "logo@3x.png")
        BACKGROUND_PATH = os.path.join(BASE_DIR, "static", "realestate", "background.png")
    else:
        qr_url = f"https://itmgroup.mx/directorio/{persona}/"
        ORG_NAME = "ITM Group"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICON_PATH = os.path.join(BASE_DIR, "static", "assets", "isoazul.png")
        LOGO_PATH = os.path.join(BASE_DIR, "static", "assets", "logo.png")
        LOGO_2X_PATH = os.path.join(BASE_DIR, "static", "assets", "logo@2x.png")
        LOGO_3X_PATH = os.path.join(BASE_DIR, "static", "assets", "logo@3x.png")
        BACKGROUND_PATH = os.path.join(BASE_DIR, "static", "assets", "background.png")

    # Crear StoreCard
    card = StoreCard()
    card.addSecondaryField("nombre", nombre, "Name")
    card.addSecondaryField("cargo", cargo, "Position")

    passfile = Pass(
        card,
        passTypeIdentifier=PASS_TYPE_IDENTIFIER,
        organizationName=ORG_NAME,
        teamIdentifier=TEAM_IDENTIFIER
    )
    passfile.serialNumber = persona
    passfile.description = "Directorio"

    passfile.barcode = Barcode(
        message=qr_url,
        format="PKBarcodeFormatQR",
        altText=cargo
    )
    #For LocalHost:
    # icon_path = os.path.join("certificates", "logo-ITM-Group-Blanco.png")
    # logo_path = os.path.join("certificates", "logo-ITM-Group-Blanco.png")

    # passfile.addFile("icon.png", open(icon_path, "rb"))
    # passfile.addFile("logo.png", open(logo_path, "rb"))
    # CERT_PATH = os.path.join(".", "certificates", "cert.pem")
    # KEY_PATH = os.path.join(".", "certificates", "key.pem")
    # WWDR_PATH = os.path.join(".", "certificates", "wwdr.pem")
    
    # Cargar imágenes dinámicamente
    passfile.addFile("icon.png", open(ICON_PATH, "rb"))
    passfile.addFile("logo.png", open(LOGO_PATH, "rb"))
    passfile.addFile("logo@2x.png", open(LOGO_2X_PATH, "rb"))
    passfile.addFile("logo@3x.png", open(LOGO_3X_PATH, "rb"))
    passfile.addFile("background.png", open(BACKGROUND_PATH, "rb"))
    passfile.addFile("strip.png", open(BACKGROUND_PATH, "rb"))

    # Generar archivo .pkpass
        #For Localhost
    # passfile.create(
    #     CERT_PATH,       # certificado
    #     KEY_PATH,        # clave privada
    #     WWDR_PATH,       # certificado WWDR
    #     None,  # contraseña original del .p12
    #     filename         # archivo de salida
    # )
    filename = f"{persona}.pkpass"
    CERT_P12_PATH = "/etc/secrets/cert.pem"
    KEY_PATH      = "/etc/secrets/key.pem"
    WWDR_PEM_PATH = "/etc/secrets/wwdr.pem"

    passfile.create(CERT_P12_PATH, KEY_PATH, WWDR_PEM_PATH, None, filename)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            print(f"No se pudo borrar {filename}: {e}")
        return response

    return send_file(
        filename,
        mimetype="application/vnd.apple.pkpass",
        as_attachment=True,
        download_name="directorio.pkpass"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
