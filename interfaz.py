# Eres libre de usar tu imaginación aquí
# Imprime aquí mensajes en pantalla que guien a un usuario a usar tu sistema de
# recomendaciones.

# En este archivo debes mandar llamar a los dos módulos:
#    libros y recomendaciones
# ya que los necesitaras para darle respuestas al usuario.

# Debes darle un mensaje al usuario con respecto a lo que hace tu programa.
# Debes preguntar si desea un resumen of palabras de un libro o si desea
# recomendaciones de libros en base a un libro que le haya gustado.
# Debes mostrar una lista con índices y nombres de los libros.

# Si desea un resumen debes preguntarle de qué libro (que te de el índice
# correspondiente) y cuantas palabras desea y despues imprimir la información
# con un formato bonito.

# Si desea recomendaciones de libro: pregúntale que libro le gusta (que te de
# un índice de acuerdo a la lista que le presentaste) y despues le preguntas
# cuantos libros quiere que le recomiendes. Posteriormente, le muestras los
# nombres de los libros recomendados con un buen formato.

import libros
import recomendaciones

print("=" * 55)
print("   Sistema de Recomendaciones de Libros - Gutenberg")
print("=" * 55)
print("Este programa analiza libros descargados del Proyecto")
print("Gutenberg y te ofrece resúmenes y recomendaciones.")
print("=" * 55)

# Crear lista de libros desde el directorio Books/
lista_libros = libros.crear_lista_libros_ingles('Books/')

if not lista_libros:
    print("\nNo se encontraron libros en la carpeta 'Books/'.")
    print("Ejecuta primero get_books.py para descargar libros.")
    exit()

# Crear recomendador y calcular pesos TF-IDF
rec = recomendaciones.Recomendador(lista_libros)
print("\nProcesando libros, por favor espera...")
rec.set_pesos()
print("Listo!\n")

# Mostrar lista de libros disponibles
print("Libros disponibles:")
print("-" * 40)
rec.mostrar_libros()
print("-" * 40)

while True:
    print("\n¿Qué deseas hacer?")
    print("  1. Ver resumen de un libro (palabras más representativas)")
    print("  2. Obtener recomendaciones de libros similares")
    print("  3. Salir")

    opcion = input("\nElige una opción (1, 2 o 3): ").strip()

    if opcion == "1":
        idx = int(input("Ingresa el índice del libro: "))
        num = int(input("¿Cuántas palabras deseas en el resumen?: "))
        palabras = rec.resumen(idx, num)
        print(f"\nResumen del libro '{lista_libros[idx].name}':")
        print("=" * 50)
        print("  " + ", ".join(palabras))
        print("=" * 50)

    elif opcion == "2":
        idx = int(input("Ingresa el índice del libro que te gustó: "))
        num = int(input("¿Cuántos libros quieres que te recomiende?: "))
        recomendados = rec.libros_similares(idx, num)
        print(f"\nBasado en '{lista_libros[idx].name}', te recomendamos:")
        print("=" * 50)
        for i, nombre in enumerate(recomendados, 1):
            print(f"  {i}. {nombre}")
        print("=" * 50)

    elif opcion == "3":
        print("\n¡Hasta luego!")
        break

    else:
        print("Opción no válida. Por favor elige 1, 2 o 3.")
