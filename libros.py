from pathlib import Path
from string import punctuation


class Libro:
    def __init__(self, name: str, filename: str) -> None:
        """Crear atributos públicos """
        self.name = name
        self.filename = filename
        self.CARACTERES_ESPECIALES: str | None = None
        self.STOPWORDS: list[str] | None = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"El nombre debe ser un string, se recibió {type(value).__name__}")
        self._name = value

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"El filename debe ser un string, se recibió {type(value).__name__}")
        if not Path(value).exists():
            raise FileNotFoundError(f"El archivo '{value}' no existe")
        self._filename = value

    def _limpiar_linea(self, linea: str) -> str:
        """Este método toma una línea de texto (str) y elimina los caracteres
        en `self.CARACTERES_ESPECIALES`.

        """
        for char in self.CARACTERES_ESPECIALES:
            linea = linea.replace(char, ' ')
        # Elimina caracteres no-alfabéticos Unicode (comillas tipográficas, guiones, etc.)
        linea = ''.join(c if c.isalpha() or c.isspace() else ' ' for c in linea)
        return linea

    def _limpiar_tokens(self, tokens: list[str]) -> list[str]:
        """Este método recibe una lista de palabras (`tokens`) y elimina
        aquellas que se encuentran en `self.STOPWORDS` modificando la lista
        original. (regresa lista de palabras sin stopwords)

        """
        tokens[:] = [t for t in tokens if t not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea: str) -> list[str]:
        """Limpia una línea de texto regresando tokens  limpios. La limpieza
        debe considerar eliminar espacios blancos al principio y final de la
        línea, convertir a minúsculas, eliminar caracteres especiales, crear
        tokens y eliminar stopwords en estos tokens.

        Este método debe aplicar los métodos anteriores donde sea necesario.
        Debe regresar tokens limpios (lista de strings).

        """
        # eliminar espacios blancos al principio y final de la línea
        linea = linea.strip()

        # convierte la linea a minúsculas
        linea = linea.lower()

        # elimina los caracteres especiales
        linea = self._limpiar_linea(linea)

        # obten tokens: transforma la linea en una lista de palabras
        tokens = linea.split()

        # limpia la lista de tokens
        self._limpiar_tokens(tokens)
        return tokens

    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista, es decir, debe regresar una lista cuyos
        elementos son las líneas no vacías del libro (el primer elemento es la
        primer línea no vacía y así sucesivamente).

        """
        lineas = []
        with open(self.filename, encoding='utf-8', errors='ignore') as f:
            for linea in f:
                if linea.strip():
                    lineas.append(linea)
        return lineas

    def preprocesar_libro(self) -> dict[str, int]:
        """Regresa un diccionario de palabras relevantes del libro como llaves
        (los tokens limpios) y sus respectivas frecuencias como valores. Por
        ejemplo, puede regresar:
            {'shrek': 55, 'fiona': 43, 'caminando': 8}

        Para hacer esto, aplica `preprocesar_linea` a cada linea del `libro`
        agregando cada token limpio con un valor de 1 al diccionario si la
        palabra no existe o aumentado el contador de la palabra correspondiente
        en caso contrario.

        """
        diccionario = {}
        for linea in self.leer_libro():
            tokens = self._preprocesar_linea(linea)
            for token in tokens:
                diccionario[token] = diccionario.get(token, 0) + 1
        return diccionario

    def __str__(self) -> str:
        """Regresa la representación de este objeto en forma de un string.

        Esta es una representación informal que tiene como objetivo que el
        objeto sea entendible para el usuario cuando utilizamos `print` (esta
        función se ejecuta cuando utilizamos ese comando).

        Ver archivo: `Codes/clase_grupo.py` para un ejemplo.

        O bien puedes ver:
          https://realpython.com/python-classes/#special-methods-and-protocols

        """
        return f"Libro: {self.name}"

    def __repr__(self) -> str:
        """Regresa la representación formal del objeto.

        En esta función regresamos un string que tome la forma en la que
        creariamos esta instancia.

        Ver archivo: `Codes/clase_grupo.py` para un ejemplo.

        O bien puedes ver:
          https://realpython.com/python-classes/#special-methods-and-protocols

        """
        return f"Libro(name={self.name!r}, filename={self.filename!r})"

# Los libros del proyecto Gutenberg empiezan dando información sobre el
# copyright y los créditos. El contenido se encuentra después de una línea que
# inicia con `*** START` y antes de la linea `*** END`. Esto debe
# considerarse al momento de leer el libro. Por lo tanto, reescribimos el
# método copprespondiente.
class LibroGutenberg(Libro):
    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista. Además, empieza a agregar solo despues de
        la línea que comienza con `*** START` y antes de la línea `*** END`.

        (Debe regresar una lista cuyos elementos son las líneas no vacías del
        libro que se encuentran entre las líneas `*** START` y `*** END`.)

        """
        lineas = []
        dentro = False
        with open(self.filename, encoding='utf-8', errors='ignore') as f:
            for linea in f:
                if '*** START' in linea:
                    dentro = True
                    continue
                if '*** END' in linea:
                    break
                if dentro and linea.strip():
                    lineas.append(linea)
        return lineas

# Los libros en distintos idiomas tienen distintos `STOPWORDS`.
class LibroEnglish(LibroGutenberg):
    # Palabras comunes no cubiertas por la lista base de NLTK
    _EXTRA_EN = {
        'one', 'yet', 'upon', 'also', 'may', 'might', 'must', 'shall',
        'would', 'could', 'even', 'still', 'though', 'however', 'thus',
        'indeed', 'perhaps', 'whether', 'without', 'every', 'much', 'many',
        'well', 'us', 'mr', 'mrs', 'said', 'unto', 'thy', 'thou', 'thee',
        'hath', 'ye', 'doth', 'whose', 'whilst', 'among', 'therefore',
        'hence', 'wherefore', 'thereof', 'hereby', 'thereby', 'wherein',
    }

    def __init__(self, name: str, filename: str) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en ingles (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        from nltk.corpus import stopwords
        self.STOPWORDS = set(stopwords.words('english')) | self._EXTRA_EN

class LibroSpanish(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en español (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        from nltk.corpus import stopwords
        self.STOPWORDS = set(stopwords.words('spanish'))

class LibroFrench(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en francés (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        from nltk.corpus import stopwords
        self.STOPWORDS = set(stopwords.words('french'))

# La siguiente función asume que todos los libros se encuentran en el
# directorio `directory`, tienen extensión `txt` y todos son en inglés.
def crear_lista_libros_ingles(directory: str, caract_especiales: str = punctuation) -> list[LibroEnglish]:
    """Crea una lista de instancias `LibroEnglish` a partir de libros
    localizados en `directory`.

    No ocupas modificar esta función, se encuentra ya implementada.

    """
    libros = []
    path = Path(directory)
    for file in path.glob('*.txt'):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros
