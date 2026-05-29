import os
import re
import math
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords

NUM_LIBROS = 100
CARPETA_LIBROS = "libros"

os.makedirs(CARPETA_LIBROS, exist_ok=True)

# OBTENER LOS LIBROS MAS DESCARGADOS
def obtener_top_libros():
    url = "https://www.gutenberg.org/browse/scores/top"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    libros = []
    listas = soup.find_all("ol")
    for lista in listas:
        enlaces = lista.find_all("a")
        for enlace in enlaces:
            href = enlace.get("href")
            if href and "/ebooks/" in href:
                libro_id = href.split("/")[-1]
                titulo = enlace.text
                libros.append((libro_id, titulo))
    return libros[:NUM_LIBROS]

# DESCARGAR LIBROS
def descargar_libro(libro_id, titulo):
    posibles_urls = [
        f"https://www.gutenberg.org/files/{libro_id}/{libro_id}-0.txt",
        f"https://www.gutenberg.org/files/{libro_id}/{libro_id}.txt",
        f"https://www.gutenberg.org/cache/epub/{libro_id}/pg{libro_id}.txt"
    ]
    for url in posibles_urls:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                nombre = re.sub(r'[\\/*?:"<>|]', "", titulo)
                ruta = os.path.join(
                    CARPETA_LIBROS,
                    f"{nombre}.txt"
                )
                with open(
                    ruta,
                    "w",
                    encoding="utf8",
                    errors="ignore"
                ) as f:
                    f.write(r.text)
                print("Descargado:", titulo)
                return ruta
        except:
            pass
    return None

# PREPROCESAMIENTO

stop_words = set(stopwords.words("english"))
def procesar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    tokens = texto.split()
    tokens = [
        t
        for t in tokens
        if t not in stop_words
        and len(t) > 2
    ]
    return tokens

# CARGAR LIBROS
def cargar_libros():
    libros = {}
    archivos = os.listdir(CARPETA_LIBROS)
    for archivo in archivos:
        ruta = os.path.join(CARPETA_LIBROS, archivo)
        with open(
            ruta,
            encoding="utf8",
            errors="ignore"
        ) as f:
            texto = f.read()
        tokens = procesar_texto(texto)
        libros[archivo] = tokens
    return libros

# DICCIONARIO GLOBAL
def crear_diccionario(libros):
    vocabulario = set()
    for palabras in libros.values():
        vocabulario.update(palabras)
    return sorted(vocabulario)