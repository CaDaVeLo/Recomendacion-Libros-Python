import os
import re
import requests

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# Carpeta donde se guardarán los libros
DIRECTORY = "Books/"

# Crea la carpeta si no existe
os.makedirs(DIRECTORY, exist_ok=True)

stop_words = set(stopwords.words("english"))

def get_links(n: int | list[int] = -1) -> tuple[list[str], list[str]]:
    """Obtiene los links y títulos de los libros más descargados
    del proyecto Gutenberg.
    """

    # URL de los libros más descargados
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        # Realiza la petición a la página
        response = requests.get(url)
        # Convierte el HTML en un objeto navegable
        parser = BeautifulSoup(response.text,'html.parser')
        # Lista donde se guardarán las ligas
        links = []
        # Lista donde se guardarán los nombres
        titles = []
        # Busca la primera lista ordenada
        lista = parser.find("ol")
        # Busca todos los enlaces dentro de la lista
        enlaces = lista.find_all("a")
        # Recorre cada enlace encontrado
        for enlace in enlaces:
            
            href = enlace.get("href")
            # Verifica que sea un enlace válido
            if href and "/ebooks/" in href:
                # Obtiene el id del libro
                libro_id = href.split("/")[-1]
                # Obtiene el nombre del libro
                titulo = enlace.text
                # Posibles URLs del txt
                posibles_urls = [f"https://www.gutenberg.org/cache/epub/{libro_id}/pg{libro_id}.txt",f"https://www.gutenberg.org/files/{libro_id}/{libro_id}-0.txt",f"https://www.gutenberg.org/files/{libro_id}/{libro_id}.txt"]

                # Busca cuál URL funciona
                for posible_url in posibles_urls:
                    try:
                        r = requests.get(posible_url,timeout=15)
                        if r.status_code == 200:
                            # Guarda el link válido
                            links.append(posible_url)
                            # Limpia caracteres inválidos
                            nombre = re.sub(r'[\\/*?:"<>|]',"",titulo)
                            # Agrega extensión txt
                            titles.append(f"{nombre}.txt")
                            # Sale del ciclo
                            break
                    # Si falla intenta otra URL
                    except:
                        pass
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
    except requests.exceptions.RequestException:
        print("wrong url for Gutenberg project")

def download_file(url, name, directory):
    """Guarda un archivo que se encuentra en un `url` bajo el nombre que demos
    en `name` en el directorio deseado.
    """
    response = requests.get(url,stream=True)
   
    name = directory + name
    
    with open(name, mode='wb') as file:
        # Descarga el archivo por bloques
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
    print(f"Downloaded file: {name}")

def store_files(links, names, directory='./'):
    """Guarda cada liga de la lista de ligas `links` en la computadora
    utilizando el directorio deseado y cada uno de los nombres en names.
    """
    # Recorre links y nombres al mismo tiempo
    for url, name in zip(links, names):
        # Descarga cada libro
        download_file(url,name,directory)

def process_text(texto):
    """Limpia y tokeniza un texto."""
    # Convierte a minúsculas
    texto = texto.lower()
    # Elimina caracteres especiales
    texto = re.sub(r'[^a-z\s]',' ',texto)
    # Convierte el texto en tokens
    tokens = texto.split()
    # Elimina stopwords y palabras cortas
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    return tokens

def load_books(directory='./'):
    """Carga y procesa todos los libros."""
    # Diccionario de libros
    books = {}
    # Recorre los archivos del directorio
    for archivo in os.listdir(directory):
        # Ruta completa
        ruta = os.path.join(directory,archivo)
        # Abre el archivo
        with open(ruta,encoding="utf8",errors="ignore") as f:
            # Lee el contenido
            texto = f.read()
        # Procesa el texto
        tokens = process_text(texto)
        # Guarda el libro procesado
        books[archivo] = tokens
    return books


def create_dictionary(books):
    """Crea el vocabulario global."""
    # Conjunto de palabras únicas
    vocabulary = set()
    # Recorre los libros
    for palabras in books.values():
        # Agrega palabras al vocabulario
        vocabulary.update(palabras)
    # Devuelve lista ordenada
    return sorted(vocabulary)

def main(n=-1, directory='./'):
    # Obtiene los links y nombres
    links, titles = get_links(n)
    print(f"Se encontraron {len(links)} libros")
    # Descarga los libros
    store_files(links,titles,directory)
    print("Procesando libros...")
    # Carga los libros
    books = load_books(directory)
    print(f"Libros procesados: {len(books)}")
    # Crea el vocabulario
    vocabulary = create_dictionary(books)
    print(f"Palabras únicas: {len(vocabulary)}")
    print("Done")


if __name__ == '__main__':
    # Carpeta donde se guardarán
    directory = 'Books/'
    # Libros a descargar
    n = range(1, 6)
    # Ejecuta el programa
    main(n, directory)