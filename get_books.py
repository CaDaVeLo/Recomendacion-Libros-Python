import os
import re
import requests

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def get_links(n: int | list[int] = -1) -> tuple[ list[str], list[str] ]:
    """Obtiene los urls y los nombres de los libros del proyecto de Gutenberg
    deseados

    Los libros se encuentran en formato txt bajo la sección descargados
    frecuentemente en:
        https://www.gutenberg.org/browse/scores/top.

    Los números `n` deben corresponder a los números en esta lista (empezando
    con uno).

    Parameters
    ----------
    n : int | list[int], optional
        Un entero o lista de enteros con los números de libros deseados
        Escoge -1 (default) si se desean todos los libros.

    Returns
    ------
    links : list[str]
        Ligas a los archivos txt de los libros.
    titles : list[str]
        Títulos de los libros
    """
    # Los libros top en el proyecto Gutenberg se encuentran aquí:
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        response = requests.get(url)

        # Parsear el contenido con BeautifulSoup
        parser = BeautifulSoup(response.text, 'html.parser')

        # Obten las ligas de los libros y sus nombres
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
                # Limpia el nombre del libro
                titulo = re.sub(r'[\\/:*?"<>|]', '', enlace.text)
                titulo = re.sub(r'\s+', ' ', titulo).strip()
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

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")
        return [], []

def download_file(url: str, name: str, directory: str) -> None:
    """Descarga un archivo desde una URL y lo guarda en el directorio indicado.

    Parameters
    ----------
    url : str
        URL del archivo a descargar.
    name : str
        Nombre con el que se guardará el archivo.
    directory : str
        Ruta del directorio donde se guardará el archivo.

    Returns
    -------
    None
    """
    response = requests.get(url, stream=True)
    name = os.path.join(directory, name)
    with open(name, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):  #10kb chunks
            file.write(chunk)
    print(f"Downloaded file: {name}")

def store_files(links: list[str], names: list[str], directory: str = './') -> None:
    """Descarga en paralelo los archivos de la lista de URLs y los guarda con
    sus respectivos nombres en el directorio indicado.

    Parameters
    ----------
    links : list[str]
        Lista de URLs de los archivos a descargar.
    names : list[str]
        Lista de nombres con los que se guardarán los archivos,
        en el mismo orden que `links`.
    directory : str, optional
        Ruta del directorio donde se guardarán los archivos (default './').

    Returns
    -------
    None
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

def main(n: int | list[int] | range = -1, directory: str = './') -> None:
    os.makedirs(directory, exist_ok=True)
    links, titles = get_links(n)
    store_files(links, titles, directory)
    print("Done")

if __name__ == '__main__':
    directory = 'Books/'
    cantidad = int(input("¿Cuántos libros deseas descargar?: "))
    n = range(1, cantidad + 1)
    main(n, directory)
