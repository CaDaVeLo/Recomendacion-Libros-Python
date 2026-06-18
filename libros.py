from pathlib import Path
from string import punctuation


class Libro:
    def __init__(self, name: str, filename: str) -> None:
        """Inicializa un libro con su nombre y ruta de archivo.

        Parameters
        ----------
        name : str
            Nombre del libro.
        filename : str
            Ruta al archivo de texto del libro.
        """
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
        """Elimina los caracteres especiales de una línea de texto.

        Sustituye cada carácter en ``self.CARACTERES_ESPECIALES`` por un
        espacio y elimina cualquier carácter no-alfabético Unicode.

        Parameters
        ----------
        linea : str
            Línea de texto a limpiar.

        Returns
        -------
        str
            Línea de texto sin caracteres especiales.
        """
        for char in self.CARACTERES_ESPECIALES:
            linea = linea.replace(char, ' ')
        # Elimina caracteres no-alfabéticos Unicode (comillas tipográficas, guiones, etc.)
        linea = ''.join(c if c.isalpha() or c.isspace() else ' ' for c in linea)
        return linea

    def _limpiar_tokens(self, tokens: list[str]) -> list[str]:
        """Elimina las stopwords de una lista de tokens, modificando la lista
        original.

        Parameters
        ----------
        tokens : list[str]
            Lista de palabras a filtrar.

        Returns
        -------
        list[str]
            Lista de tokens sin stopwords.
        """
        tokens[:] = [t for t in tokens if t not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea: str) -> list[str]:
        """Aplica el pipeline completo de limpieza a una línea de texto.

        Elimina espacios al inicio y al final, convierte a minúsculas, elimina
        caracteres especiales, tokeniza y descarta stopwords.

        Parameters
        ----------
        linea : str
            Línea de texto a preprocesar.

        Returns
        -------
        list[str]
            Lista de tokens limpios.
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
        """Lee el archivo del libro y devuelve sus líneas no vacías.

        Returns
        -------
        list[str]
            Lista de líneas no vacías del libro, en el orden original.
        """
        lineas = []
        with open(self.filename, encoding='utf-8', errors='ignore') as f:
            for linea in f:
                if linea.strip():
                    lineas.append(linea)
        return lineas

    def preprocesar_libro(self) -> dict[str, int]:
        """Construye un diccionario de frecuencias de palabras relevantes del
        libro.

        Lee el libro, aplica el preprocesamiento a cada línea y cuenta las
        ocurrencias de cada token limpio.

        Returns
        -------
        dict[str, int]
            Diccionario con tokens limpios como llaves y sus frecuencias como
            valores.
        """
        diccionario = {}
        for linea in self.leer_libro():
            tokens = self._preprocesar_linea(linea)
            for token in tokens:
                diccionario[token] = diccionario.get(token, 0) + 1
        return diccionario

    def __str__(self) -> str:
        """Devuelve la representación informal del libro para el usuario.

        Returns
        -------
        str
            Cadena con el nombre del libro en formato legible.
        """
        return f"Libro: {self.name}"

    def __repr__(self) -> str:
        """Devuelve la representación formal del objeto, reproducible en código.

        Returns
        -------
        str
            Cadena que muestra cómo recrear esta instancia.
        """
        return f"Libro(name={self.name!r}, filename={self.filename!r})"

# Los libros del proyecto Gutenberg empiezan dando información sobre el
# copyright y los créditos. El contenido se encuentra después de una línea que
# inicia con `*** START` y antes de la linea `*** END`. Esto debe
# considerarse al momento de leer el libro. Por lo tanto, reescribimos el
# método copprespondiente.
class LibroGutenberg(Libro):
    def leer_libro(self) -> list[str]:
        """Lee el archivo del libro devolviendo solo las líneas entre las
        marcas ``*** START`` y ``*** END`` del Proyecto Gutenberg.

        Returns
        -------
        list[str]
            Lista de líneas no vacías del contenido del libro, excluyendo
            el encabezado y pie de página de Gutenberg.
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
        """Inicializa el libro cargando las stopwords en inglés con NLTK.

        Parameters
        ----------
        name : str
            Nombre del libro.
        filename : str
            Ruta al archivo de texto del libro.
        """
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en ingles (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        from nltk.corpus import stopwords
        self.STOPWORDS = set(stopwords.words('english')) | self._EXTRA_EN

class LibroSpanish(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        """Inicializa el libro cargando las stopwords en español con NLTK.

        Parameters
        ----------
        name : str
            Nombre del libro.
        filename : str
            Ruta al archivo de texto del libro.
        """
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en español (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        from nltk.corpus import stopwords
        self.STOPWORDS = set(stopwords.words('spanish'))

class LibroFrench(LibroGutenberg):
    def __init__(self, name: str, filename: str) -> None:
        """Inicializa el libro cargando las stopwords en francés con NLTK.

        Parameters
        ----------
        name : str
            Nombre del libro.
        filename : str
            Ruta al archivo de texto del libro.
        """
        super().__init__(name, filename)
        # Agregar aquí los STOPWORDS en francés (utiliza nltk).
        # (No ocupas hacer nada más que eso)
        from nltk.corpus import stopwords
        self.STOPWORDS = set(stopwords.words('french'))

# La siguiente función asume que todos los libros se encuentran en el
# directorio `directory`, tienen extensión `txt` y todos son en inglés.
def crear_lista_libros_ingles(directory: str, caract_especiales: str = punctuation) -> list[LibroEnglish]:
    """Crea una lista de instancias ``LibroEnglish`` a partir de los archivos
    .txt encontrados en un directorio.

    Parameters
    ----------
    directory : str
        Ruta al directorio que contiene los archivos de texto.
    caract_especiales : str, optional
        Caracteres especiales a eliminar durante el preprocesamiento
        (default: ``string.punctuation``).

    Returns
    -------
    list[LibroEnglish]
        Lista con una instancia de ``LibroEnglish`` por cada archivo .txt
        encontrado en `directory`.
    """
    libros = []
    path = Path(directory)
    for file in path.glob('*.txt'):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros
