import math
from libros import Libro


class Recomendador:
    def __init__(self, libros: list[Libro]) -> None:
        """Inicializa el recomendador con una colección de libros.

        Parameters
        ----------
        libros : list[Libro]
            Lista de instancias de tipo ``Libro`` sobre las que se calcularán
            las recomendaciones.
        """
        self.libros = libros
        self._pesos = None  # Se calcularan con un setter (ver `set_pesos`)

    def set_pesos(self) -> None:
        """Calcula y almacena los pesos TF-IDF para todos los libros de la
        colección.

        El peso de cada palabra en un libro se calcula como:
            W(i,j) = TF(i,j) * ln(1 + N / DF(i))

        Returns
        -------
        None
        """
        N = len(self.libros)
        freq_dicts = [libro.preprocesar_libro() for libro in self.libros]

        # Frecuencia de documento: cuántos libros contienen cada palabra
        df = {}
        for freq in freq_dicts:
            for word in freq:
                df[word] = df.get(word, 0) + 1

        # W(i,j) = TF(i,j) * ln(1 + N / DF(i))
        self._pesos = []
        for freq in freq_dicts:
            total = sum(freq.values()) or 1
            pesos_libro = {
                word: (count / total) * math.log(1 + N / df[word])
                for word, count in freq.items()
            }
            self._pesos.append(pesos_libro)

    def get_pesos(self) -> list[dict[str, float]] | None:
        """Devuelve los pesos TF-IDF calculados por ``set_pesos``.

        Returns
        -------
        list[dict[str, float]] | None
            Lista de diccionarios con los pesos por libro, o ``None`` si
            ``set_pesos`` no ha sido llamado.
        """
        return self._pesos

    def _producto_punto(self, idx_1: int, idx_2: int) -> float:
        """Calcula el producto punto entre los vectores de pesos de dos libros.

        Parameters
        ----------
        idx_1 : int
            Índice del primer libro en ``self.libros``.
        idx_2 : int
            Índice del segundo libro en ``self.libros``.

        Returns
        -------
        float
            Producto punto entre los vectores TF-IDF de los dos libros.
        """
        pesos_1 = self._pesos[idx_1]
        pesos_2 = self._pesos[idx_2]
        return sum(pesos_1.get(word, 0) * pesos_2.get(word, 0) for word in pesos_1)

    def _similitud(self, idx_1: int, idx_2: int) -> float:
        """Calcula la similitud coseno entre dos libros.

        Parameters
        ----------
        idx_1 : int
            Índice del primer libro en ``self.libros``.
        idx_2 : int
            Índice del segundo libro en ``self.libros``.

        Returns
        -------
        float
            Similitud coseno entre los vectores TF-IDF de los dos libros,
            en el rango [0, 1].
        """
        dot = self._producto_punto(idx_1, idx_2)
        norm_1 = math.sqrt(self._producto_punto(idx_1, idx_1))
        norm_2 = math.sqrt(self._producto_punto(idx_2, idx_2))
        if norm_1 == 0 or norm_2 == 0:
            return 0.0
        return dot / (norm_1 * norm_2)

    def mostrar_libros(self) -> None:
        """Imprime el índice y nombre de cada libro de la colección.

        Returns
        -------
        None
        """
        for i, libro in enumerate(self.libros):
            print(f"  {i}: {libro.name}")

    def resumen(self, idx_libro: int, num_palabras: int) -> list[str]:
        """Devuelve las palabras más representativas de un libro según sus
        pesos TF-IDF.

        Parameters
        ----------
        idx_libro : int
            Índice del libro en ``self.libros``.
        num_palabras : int
            Número de palabras a incluir en el resumen.

        Returns
        -------
        list[str]
            Lista de las ``num_palabras`` palabras con mayor peso TF-IDF.
        """
        pesos = self._pesos[idx_libro]
        sorted_words = sorted(pesos.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:num_palabras]]

    def libros_similares(self, idx_libro: int, num_libros: int) -> list[str]:
        """Devuelve los libros más similares a uno dado, ordenados por
        similitud coseno descendente.

        Parameters
        ----------
        idx_libro : int
            Índice del libro de referencia en ``self.libros``.
        num_libros : int
            Número de recomendaciones a devolver. Si excede el total de
            libros disponibles (excluyendo el libro de referencia), se
            devuelven todos los disponibles.

        Returns
        -------
        list[str]
            Lista con los nombres de los ``num_libros`` libros más similares,
            sin incluir el libro de referencia.
        """
        num_libros = min(num_libros, len(self.libros) - 1)
        similitudes = []
        for i in range(len(self.libros)):
            if i != idx_libro:
                sim = self._similitud(idx_libro, i)
                similitudes.append((i, sim))
        similitudes.sort(key=lambda x: x[1], reverse=True)
        return [self.libros[i].name for i, _ in similitudes[:num_libros]]
