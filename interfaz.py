# Eres libre de usar tu imaginación aquí
# Imprime aquí mensajes en pantalla que guien a un usuario a usar tu sistema de
# recomendaciones.

# En este archivo debes mandar llamar a los dos módulos:
#    libros y recomendaciones
# ya que los necesitaras para darle respuestas al usuario.

# Debes darle un mensaje al usuario con respecto a lo que hace tu programa.
# Debes preguntar si desea un resumen de palabras de un libro o si desea
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

ANCHO = 60

def separador(char="-"):
    print(char * ANCHO)

def titulo(texto, char="="):
    print(char * ANCHO)
    print(f"  {texto}")
    print(char * ANCHO)

def pedir_indice(prompt, maximo):
    while True:
        try:
            val = int(input(prompt))
            if 0 <= val <= maximo:
                return val
            print(f"  Error: ingresa un número entre 0 y {maximo}.")
        except ValueError:
            print("  Error: ingresa un número entero válido.")

def pedir_entero_positivo(prompt):
    while True:
        try:
            val = int(input(prompt))
            if val > 0:
                return val
            print("  Error: ingresa un número mayor a 0.")
        except ValueError:
            print("  Error: ingresa un número entero válido.")

def mostrar_menu():
    separador()
    print("  MENU PRINCIPAL")
    separador()
    print("  1. Ver resumen de un libro")
    print("  2. Obtener recomendaciones de libros similares")
    print("  3. Mostrar lista de libros")
    print("  0. Salir")
    separador()

def flujo_resumen(rec, lista):
    titulo("RESUMEN DE LIBRO")
    rec.mostrar_libros()
    separador()
    idx = pedir_indice("Índice del libro: ", len(lista) - 1)
    num = pedir_entero_positivo("¿Cuántas palabras deseas en el resumen?: ")
    palabras = rec.resumen(idx, num)
    print(f"\nPalabras más representativas de '{lista[idx].name}':")
    titulo(", ".join(palabras), char="-")

def flujo_recomendaciones(rec, lista):
    titulo("RECOMENDACIONES")
    rec.mostrar_libros()
    separador()
    idx = pedir_indice("Índice del libro que te gustó: ", len(lista) - 1)
    num = pedir_entero_positivo("¿Cuántos libros quieres que te recomiende?: ")
    recomendados = rec.libros_similares(idx, num)
    print(f"\nBasado en '{lista[idx].name}', te recomendamos:")
    separador()
    for i, nombre in enumerate(recomendados, 1):
        print(f"  {i}. {nombre}")
    separador()


# ──────────────────────Inicio─────────────────────────────── #
titulo("Sistema de Recomendaciones de Libros - Gutenberg")
print("  Analiza libros del Proyecto Gutenberg y ofrece")
print("  resúmenes y recomendaciones basadas en TF-IDF.")
separador()

lista_libros = libros.crear_lista_libros_ingles('Books/')

if not lista_libros:
    print("\nNo se encontraron libros en 'Books/'.")
    print("Ejecuta primero get_books.py para descargar libros.")
    exit()

rec = recomendaciones.Recomendador(lista_libros)
print("\nProcesando libros, por favor espera...")
rec.set_pesos()
print(f"Listo! Se cargaron {len(lista_libros)} libros.\n")

# ──────────────────────Bucle Principal─────────────────────────────── #
while True:
    mostrar_menu()
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        flujo_resumen(rec, lista_libros)
    elif opcion == "2":
        flujo_recomendaciones(rec, lista_libros)
    elif opcion == "3":
        titulo("LIBROS DISPONIBLES")
        rec.mostrar_libros()
        separador()
    elif opcion == "0":
        separador()
        print("  ¡Hasta luego!")
        separador()
        break
    else:
        print("  Opción no válida. Elige 0, 1, 2 o 3.\n")
