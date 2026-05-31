import os
import re
import requests

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor

# Lista de stopwords en inglés
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
        with open(self.filename,encoding="utf8",errors="ignore") as f:
            # Lee todo el texto
            texto = f.read()
        return texto

    # Convierte el texto a minúsculas
    def convertir_minusculas(self, texto):
        return texto.lower()
    # Limpia caracteres especiales
    def limpiar_texto(self, texto):
        return re.sub(r'[^a-z\s]',' ',texto)
    
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
    
def limpiar_nombre_archivo(nombre):
    nombre = re.sub(r'[\\/:*?"<>|]', '', nombre)
    nombre = re.sub(r'\s+', ' ', nombre)
    return nombre.strip()

def get_links(n: int | list[int] = -1) -> tuple[list[str], list[str]]:
    """Obtiene los urls y los nombres de los libros del proyecto de Gutenberg
    deseados.

    Los libros se encuentran en formato txt bajo la sección descargados
    frecuentemente en:
        https://www.gutenberg.org/browse/scores/top.

    Los números `n` deben corresponder a los números en esta lista (empezando
    con uno).

    Parameters
    ----------
    n : int | list[int], optional
        Un entero o lista de enteros con los números de libros deseados.
        Escoge -1 (default) si se desean todos los libros.

    Returns
    -------
    links : list[str]
        Ligas a los archivos txt de los libros.
    titles : list[str]
        Títulos de los libros.
    """

    # Los libros top en el proyecto Gutenberg se encuentran aquí:
    url = "https://www.gutenberg.org/browse/scores/top"

    try:
        # Realiza la petición a la página
        response = requests.get(url)
        # Parsear el contenido con BeautifulSoup
        parser = BeautifulSoup(response.text,'html.parser')

        # Lista donde se guardarán las ligas
        links = []
        # Lista donde se guardarán los nombres
        titles = []

        # Busca la primera lista ordenada
        lista = parser.find("ol")
        # Busca todos los enlaces dentro de la lista
        enlaces = lista.find_all("a")
        # Determina cuántos libros buscar
        if n == -1:
            limite = len(enlaces)
        elif isinstance(n, int):
            limite = n
        else:
            limite = max(n)
        # Recorre cada enlace encontrado
        for enlace in enlaces[:limite]:
            href = enlace.get("href")
            # Verifica que sea un enlace válido
            if href and "/ebooks/" in href:
                libro_id = href.split("/")[-1]
                # Obtiene el nombre del libro
                titulo = limpiar_nombre_archivo(enlace.text)

                url_txt = f"https://www.gutenberg.org/cache/epub/{libro_id}/pg{libro_id}.txt"

                links.append(url_txt)
                titles.append(f"{titulo}.txt")
        # Si n es -1 devuelve todos
        if n == -1:
            return links, titles
        # Si n es un entero
        if isinstance(n, int):
            return [links[n - 1]], [titles[n - 1]]
        # Si n es una lista o rango
        selected_links = []
        selected_titles = []
        # Recorre los índices pedidos
        for i in n:
            selected_links.append(links[i - 1])
            selected_titles.append(titles[i - 1])
        return selected_links, selected_titles
    except Exception as e:
        print("ERROR:", e)
        return [], []

def download_file(url, name, directory):
    """Guarda un archivo que se encuentra en un `url` bajo el nombre que demos
    en `name` en el directorio deseado.
    """

    # Hace petición del archivo
    response = requests.get(url,stream=True)

    # Ruta completa donde se guardará
    name = os.path.join(directory, name)
    # Abre el archivo en modo escritura binaria
    with open(name, mode='wb') as file:
        # Descarga el archivo por bloques
        for chunk in response.iter_content(chunk_size=256 * 1024):
            file.write(chunk)

    print(f"Downloaded file: {name}")

def store_files(links, names, directory='./'):
    """Guarda cada liga de la lista de ligas `links` en la computadora
    utilizando el directorio deseado y cada uno de los nombres en names.
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(download_file, url, name, directory)
            for url, name in zip(links, names)
        ]

        for future in futures:

            try:
                future.result()

            except Exception as e:
                print("Error:", e)


def main(n=-1, directory='./'):
    os.makedirs(directory, exist_ok=True)

    # Obtiene los links y nombres
    links, titles = get_links(n)
    print(f"Se encontraron {len(links)} libros")
    print("Obteniendo links...")
    print("Links encontrados:", len(links))
    print("Titulos encontrados:", len(titles))

    # Descarga los libros
    store_files(links,titles,directory)

    print("\nLIBROS PROCESADOS\n")

    # Recorre cada archivo descargado
    for archivo in os.listdir(directory):

        # Ruta completa del archivo
        ruta = os.path.join(directory,archivo)

        # Crea un objeto Libro
        libro = Libro(ruta)

        # Obtiene tokens limpios
        tokens = libro.obtener_tokens()

        print(archivo,"->",len(tokens),"tokens")

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