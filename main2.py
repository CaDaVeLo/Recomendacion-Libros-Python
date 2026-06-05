import os
import re

from nltk.corpus import stopwords

from downloader import get_links, store_files

stop_words = set(stopwords.words("english"))


class Libro:
    def __init__(self, filename):
        """
        filename:
        Ruta del archivo txt del libro
        """
        # Guarda la ruta del libro
        self.filename = filename

    # Lee el contenido completo del libro
    def leer_libro(self):
        # Abre el archivo txt
        with open(self.filename, encoding="utf8", errors="ignore") as f:
            # Lee todo el texto
            texto = f.read()
        return texto

    # Convierte el texto a minúsculas
    def convertir_minusculas(self, texto):
        return texto.lower()

    # Limpia caracteres especiales
    def limpiar_texto(self, texto):
        return re.sub(r'[^a-z\s]', ' ', texto)

    # Convierte el texto en tokens
    def tokenizar(self, texto):
        return texto.split()

    # Elimina stopwords y palabras cortas
    def eliminar_stopwords(self, tokens):
        tokens_limpios = [t for t in tokens if t not in stop_words and len(t) > 2]
        return tokens_limpios

    # Aplica todo el preprocesamiento
    def obtener_tokens(self):
        # Lee el libro
        texto = self.leer_libro()
        # Convierte todo a minúsculas
        texto = self.convertir_minusculas(texto)
        # Limpia caracteres especiales
        texto = self.limpiar_texto(texto)
        # Convierte el texto en tokens
        tokens = self.tokenizar(texto)
        # Elimina stopwords
        tokens = self.eliminar_stopwords(tokens)
        # Regresa tokens limpios
        return tokens


def main(n=-1, directory='./'):
    os.makedirs(directory, exist_ok=True)

    # Obtiene los links y nombres
    links, titles = get_links(n)
    print(f"Se encontraron {len(links)} libros")
    print("Obteniendo links...")
    print("Links encontrados:", len(links))
    print("Titulos encontrados:", len(titles))

    # Descarga los libros
    store_files(links, titles, directory)

    print("\nLIBROS PROCESADOS\n")

    diccionario_global = {}

    # Recorre cada archivo descargado
    for archivo in os.listdir(directory):

        # Ruta completa del archivo
        ruta = os.path.join(directory, archivo)

        # Crea un objeto Libro
        libro = Libro(ruta)

        # Obtiene tokens limpios
        tokens = libro.obtener_tokens()

        print(archivo, "->", len(tokens), "tokens")

        # Acumula frecuencias en el diccionario global
        for token in tokens:
            diccionario_global[token] = diccionario_global.get(token, 0) + 1

    print("\nDiccionario global:")
    print(diccionario_global)
    print("\nDone")


if __name__ == '__main__':
    # Carpeta donde se guardarán
    directory = 'Books/'

    # Pregunta cuántos libros descargar
    cantidad = int(input("¿Cuántos libros deseas descargar?: "))

    # Libros a descargar
    n = range(1, cantidad + 1)

    # Ejecuta el programa
    main(n, directory)
