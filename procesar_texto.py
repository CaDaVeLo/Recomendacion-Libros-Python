import preprocesado


def main(filename: str) -> dict[str, int]:
    # Definir lista con caracteres especiales.
    # Utilizar los caracteres dados por `punctuation` en la librería `string`
    from string import punctuation
    caracteres_especiales = list(punctuation)

    # Definir lista con stopwords.
    # Utilizar los stopword en inglés dados en la librería nltk (como vimos en
    # clase).
    from nltk.corpus import stopwords as nltk_stopwords
    stopwords = set(nltk_stopwords.words('english'))

    # Leer el libro utilizando función correspondiente del módulo `preprocesado`
    libro = preprocesado.leer_libro(filename)

    # Preprocesar el libro obteniendo un diccionario de palabras relevantes y
    # sus frecuencias y retornar este resultado.
    # Debes utilizar el método correspondiente en `preprocesado`.
    return preprocesado.preprocesar_libro(libro, caracteres_especiales, stopwords)

if __name__ == '__main__':
    # Definir a continuación `filename`
    filename = input("Ingresa la ruta del archivo de texto: ")

    # Ahora descomenta la línea de abajo
    resultado = main(filename)
    print(resultado)

    # Una vez llenado el módulo preprocesado y este script, puedes ejecutarlo
    # escribiendo en la terminal
    # python procesar_texto
