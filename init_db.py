import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Crear tabla personas
cur.execute("""
CREATE TABLE IF NOT EXISTS personas (
    id       INTEGER PRIMARY KEY,
    nombre   TEXT NOT NULL,
    apellido TEXT NOT NULL,
    puesto   TEXT NOT NULL,
    correo   TEXT NOT NULL,
    celular  TEXT NOT NULL,
    imagen   TEXT NOT NULL
)
""")

personas = [
    (1,  "Fernanda",      "Tovar",       "Commercial Director of Real Estate and Retail",      "ftovar@itmgroup.mx",     "+5219988656453",  "/directorio/assets/images/fernanda-tovar.png"),
    (2,  "Juanli",        "Teran",       "Marketing Director",                                 "jteran@itmgroup.mx",     "+5219981671077",  "/directorio/assets/images/juanli-teran.png"),
    (3,  "Ernesto",       "Monteiro",    "Director of Operations - Port Melilla",               "emonteiro@itmgroup.mx",  "+5219982773668",  "/directorio/assets/images/ernesto-monteiro.png"),
    (4,  "Karen",         "Lopez",       "Project Management Office",                          "klopez@itmgroup.mx",     "+5219988749986",  "/directorio/assets/images/karen-lopez.png"),
    (5,  "Luis Fernando", "Paredes",     "Project Director",                                   "lparedes@itmgroup.mx",   "+5219981361305",  "/directorio/assets/images/fernando-paredes.png"),
    (6,  "Mariana",       "Perrilliat",  "VP Corporate & General Counsel",                     "mperrilliat@itmgroup.mx","+5219981090167",  "/directorio/assets/images/mariana-perrilliat.png"),
    (7,  "Mauricio",      "Hamui",       "CEO",                                                "mhh@itmgroup.mx",        "-",               "/directorio/assets/images/mauricio-hamui.png"),
    (8,  "Fernando",      "Castro",      "Finance & IT Vicepresident",                         "fcastro@itmgroup.mx",    "+5219988300748",  "/directorio/assets/images/fernando-castro.png"),
    (9,  "Maribel",       "Galicia",     "Director of Business Integration",                   "mgalicia@itmgroup.mx",   "+5215539660271",  "/directorio/assets/images/maribel-galicia.png"),
    (10, "Inaki",         "Heras",       "Corporate IT Director",                              "iheras@itmgroup.mx",     "+5219981222257",  "/directorio/assets/images/inaki-heras.png"),
    (11, "Fredy",         "Chan",        "Corporate Accounting and Tax Director",               "fchan@itmgroup.mx",      "+5219991905698",  "/directorio/assets/images/fredy-chan.png"),
    (12, "Gabriel",       "Guevara",     "Port Director - Port Taino Bay & Port Cabo Rojo",    "gguevara@itmgroup.mx",   "+5219992781442",  "/directorio/assets/images/gabriel-guevara.png"),
    (13, "German",        "Ramirez",     "Finance Corporate Director",                         "gramirez@itmgroup.mx",   "+5219982423937",  "/directorio/assets/images/german-ramirez.png"),
    (14, "Hugo",          "Morales",     "Financial Advisor",                                  "hmorales@itmgroup.mx",   "+5219982413085",  "/directorio/assets/images/hugo-morales.png"),
    (15, "Kester",        "Bodden",      "Port Director - Port Roatan",                        "kbodden@itmgroup.mx",    "+52150499619226", "/directorio/assets/images/kester-bodden.png"),
    (16, "Otto",          "Quevedo",     "Port Director - Port La Paz",                        "oquevedo@portlapaz.com", "+5219837333785",  "/directorio/assets/images/otto-quevedo.png"),
    (17, "Alicia",        "Mateos",      "Director of Sustainability and Open Enterprises",    "amateos@itmgroup.mx",    "+5219988457172",  "/directorio/assets/images/alicia-mateos.png"),
    (18, "Carla",         "Desentis",    "Corporate Strategy & Legal Director",                "cdesentis@itmgroup.mx",  "+5219988743398",  "/directorio/assets/images/carla-desentis.png"),
    (19, "Daniela",       "Munoz",       "Commercial Director of Ports and Destinations",      "dmunoz@itmgroup.mx",     "+5219831054860",  "/directorio/assets/images/daniela-munoz.png"),
    (20, "Emelyne",       "Arrieta",     "VP Construction & Development",                      "earrieta@itmgroup.mx",   "+5219983217493",  "/directorio/assets/images/emelyne-arrieta.png"),
    (21, "Adriana",       "Aguilar",     "Director of Tour and Traffic Operations",            "aaguilar@itmgroup.mx",   "+5219982462203",  "/directorio/assets/images/adriana-aguilar.png"),
    (22, "Fernanda",      "Mexia",       "Bookings Manager",                                   "fmexia@itmgroup.mx",     "+5219988744418",  "/directorio/assets/images/fernanda-mexia.png"),
    (23, "Paola",         "de la Garza", "Marketing Manager",                                  "pgarza@itmgroup.mx",     "+5219982025919",  "/directorio/assets/images/paola-garza.png"),
    (24, "Jesiel",        "Castro",      "Corp Commercial Tour Manager",                       "jcastro@itmgroup.mx",    "+5219831366833",  "/directorio/assets/images/jesiel-castro.png"),
    (25, "Gabriela",      "Rodarte",     "Commercial & Product Development Manager",           "grodarte@itmgroup.mx",   "+5219985773339",  "/directorio/assets/images/gabriela-rodarte.png"),
    (26, "Ing. Isaac",    "Hamui",       "Presidencia",                                        "lsauvinet@itmgroup.mx",  "+5219982677710",  "/directorio/assets/images/mauricio-hamui.png"),
    (27, "Herman",        "Bautista",    "ITM Delegate Spain",                                 "hbautista@itmgroup.mx",  "+34649020900",    "/directorio/assets/images/herman-bautista.png"),
    (28, "Estefania",     "Buitron",     "ITM Delegate Spain",                                 "ebuitron@itmgroup.mx",   "+5215523334351",  "/directorio/assets/images/estefania-buitron.png"),
    (29, "Isabella",      "Mogna",       "ITM Delegate Spain",                                 "imogna@itmgroup.mx",     "+34677336854",    "/directorio/assets/images/isabella-mogna.png"),
]

cur.executemany(
    "INSERT OR REPLACE INTO personas (id, nombre, apellido, puesto, correo, celular, imagen) VALUES (?, ?, ?, ?, ?, ?, ?)",
    personas
)

conn.commit()
conn.close()
print(f"Base de datos creada con {len(personas)} personas.")
