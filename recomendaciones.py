import math
from libros import Libro


class Recomendador:
    def __init__(self, libros: list[Libro]) -> None:
        """
        libros: lista con instancias de tipo `Libro`
        """
        self.libros = libros
        self._pesos = None  # Se calcularan con un setter (ver `set_pesos`)

    def set_pesos(self) -> None:
        """Calcula los pesos del algorítmo TF-IDF requeridos para las
        recomendaciones y los guarda en `self._pesos`

        """
        freq_dicts = [libro.preprocesar_libro() for libro in self.libros]
        N = len(self.libros)

        # Obtener todas las palabras únicas entre todos los libros
        all_words = set()
        for freq in freq_dicts:
            all_words.update(freq.keys())

        # Calcular IDF para cada palabra
        idf = {}
        for word in all_words:
            df = sum(1 for freq in freq_dicts if word in freq)
            idf[word] = math.log(N / (1 + df))

        # Calcular TF-IDF para cada libro
        self._pesos = []
        for freq in freq_dicts:
            total = sum(freq.values()) or 1
            pesos_libro = {}
            for word, count in freq.items():
                tf = count / total
                pesos_libro[word] = tf * idf[word]
            self._pesos.append(pesos_libro)

    def get_pesos(self) -> list[dict[str, float]] | None:
        """Regresa los pesos calculados"""
        return self._pesos

    def _producto_punto(self, idx_1:int, idx_2:int) -> float:
        """Producto punto entre los libros con índices idx_1 y idx_2."""
        pesos_1 = self._pesos[idx_1]
        pesos_2 = self._pesos[idx_2]
        return sum(pesos_1.get(word, 0) * pesos_2.get(word, 0) for word in pesos_1)

    def _similitud(self, idx_1: int, idx_2: int) -> float:
        """Similitud entre los libros con índices idx_1 y idx_2 de acuerdo a l
        cosene del ángulo que forman sus vectores.

        """
        dot = self._producto_punto(idx_1, idx_2)
        norm_1 = math.sqrt(self._producto_punto(idx_1, idx_1))
        norm_2 = math.sqrt(self._producto_punto(idx_2, idx_2))
        if norm_1 == 0 or norm_2 == 0:
            return 0.0
        return dot / (norm_1 * norm_2)

    def mostrar_libros(self) -> None:
        """Mostrarle al usuario el índice y nombre para cada libro de acuerdo a
        nuestra lista de libros `self.libros`.

        """
        for i, libro in enumerate(self.libros):
            print(f"  {i}: {libro.name}")

    def resumen(self, idx_libro: int, num_palabras: int) -> list[str]:
        """Regresa una lista con las palabras más representativas de un libro
        de acuerdo a los pesos.

        idx_libro: índice del libro cuyo resumen deseamos.
        num_palabras: número de palabras en el resumen.

        """
        pesos = self._pesos[idx_libro]
        sorted_words = sorted(pesos.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:num_palabras]]

    def libros_similares(self, idx_libro: int, num_libros: int) -> list[str]:
        """Regresa una lista con los libros más parecidos a un libro dado.

        idx_libro: índice del libro a partir del cual quiero recomendaciones.
        num_libros: número de libros en mi recomendación.


        """
        similitudes = []
        for i in range(len(self.libros)):
            if i != idx_libro:
                sim = self._similitud(idx_libro, i)
                similitudes.append((i, sim))
        similitudes.sort(key=lambda x: x[1], reverse=True)
        return [self.libros[i].name for i, _ in similitudes[:num_libros]]
