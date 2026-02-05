"""
Programa para contar palabras distintas y sus frecuencias.

Actividad 4.2 - TC4017 Calidad de Software
Tecnológico de Monterrey

Uso: python wordCount.py archivoConDatos.txt
"""

import sys
import time
import os


def read_words_from_file(filepath):
    """
    Lee palabras de un archivo de texto (una por línea).

    Args:
        filepath: Ruta al archivo

    Returns:
        Lista de palabras (strings), incluyendo líneas vacías como ''
    """
    words = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            words.append(word)
    return words


def count_words(words):
    """
    Cuenta la frecuencia de cada palabra usando algoritmo básico.
    NO usa Counter ni funciones de biblioteca.

    Args:
        words: Lista de palabras

    Returns:
        Tupla (word_counts, blank_count) donde:
        - word_counts: Lista de tuplas (palabra, conteo, primera_posicion)
        - blank_count: Número de líneas vacías
    """
    # Diccionario manual para conteo
    counts = {}
    first_position = {}
    blank_count = 0

    for i, word in enumerate(words, 1):
        if word == '':
            print(f"Error: Línea vacía en la línea {i}")
            blank_count += 1
        else:
            if word in counts:
                counts[word] = counts[word] + 1
            else:
                counts[word] = 1
                first_position[word] = i

    # Convertir a lista de tuplas
    word_counts = []
    for word, count in counts.items():
        word_counts.append((word, count, first_position[word]))

    return word_counts, blank_count


def sort_word_counts(word_counts):
    """
    Ordena las palabras por frecuencia descendente, luego alfabéticamente.
    Implementación de ordenamiento sin usar sorted() con key compleja.

    Args:
        word_counts: Lista de tuplas (palabra, conteo, posicion)

    Returns:
        Lista ordenada de tuplas (palabra, conteo)
    """
    # Crear lista para ordenar
    to_sort = []
    for word, count, pos in word_counts:
        to_sort.append((word, count, pos))

    # Bubble sort manual (sin usar sorted con key)
    length = len(to_sort)
    for i in range(length):
        for j in range(0, length - i - 1):
            # Comparar: primero por conteo descendente, luego alfabéticamente
            word1, count1, _ = to_sort[j]
            word2, count2, _ = to_sort[j + 1]

            should_swap = False
            if count1 < count2:
                should_swap = True
            elif count1 == count2:
                # Mismo conteo: ordenar alfabéticamente
                if word1 > word2:
                    should_swap = True

            if should_swap:
                to_sort[j], to_sort[j + 1] = to_sort[j + 1], to_sort[j]

    # Retornar solo palabra y conteo
    result = []
    for word, count, pos in to_sort:
        result.append((word, count))
    return result


def get_filename_without_extension(filepath):
    """Extrae el nombre del archivo sin extensión."""
    basename = os.path.basename(filepath)
    name, _ = os.path.splitext(basename)
    return name


def print_results(results):
    """
    Imprime los resultados en consola.

    Args:
        results: Diccionario con sorted_counts, blank_count, total_words,
                 filename y elapsed_time
    """
    print(f"Row Labels\tCount of {results['filename']}")
    for word, count in results['sorted_counts']:
        print(f"{word}\t{count}")
    if results['blank_count'] > 0:
        print("(blank)\t")
    print(f"Grand Total\t{results['total_words']}")
    print(f"\nTiempo transcurrido: {results['elapsed_time']:.3f} segundos")


def _build_result_lines(results):
    """Construye las líneas de resultado para escribir al archivo."""
    lines = [f"Row Labels\tCount of {results['filename']}\n"]
    for word, count in results['sorted_counts']:
        lines.append(f"{word}\t{count}\n")
    if results['blank_count'] > 0:
        lines.append("(blank)\t\n")
    lines.append(f"Grand Total\t{results['total_words']}\n")
    lines.append(f"TIEMPO\t{results['elapsed_time']:.3f}s\n")
    return lines


def write_results(results, output_path):
    """
    Escribe los resultados al archivo de salida.

    Si el archivo existe, agrega los nuevos resultados debajo.
    Si no existe, crea el archivo con el formato inicial.

    Args:
        results: Diccionario con los resultados del conteo
        output_path: Ruta del archivo de salida
    """
    result_lines = _build_result_lines(results)

    mode = 'a' if os.path.exists(output_path) else 'w'
    with open(output_path, mode, encoding='utf-8') as file:
        if mode == 'a':
            file.write("\n\n")
        file.writelines(result_lines)


def _validate_args():
    """Valida los argumentos de línea de comandos y retorna el filepath."""
    if len(sys.argv) != 2:
        print("Uso: python word_count.py archivoConDatos.txt")
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: Archivo no encontrado: {filepath}")
        sys.exit(1)
    return filepath


def main():
    """Función principal del programa."""
    filepath = _validate_args()
    start_time = time.time()

    # Leer palabras del archivo
    words = read_words_from_file(filepath)

    # Contar palabras
    word_counts, blank_count = count_words(words)

    # Ordenar por frecuencia descendente
    sorted_counts = sort_word_counts(word_counts)

    # Calcular tiempo transcurrido
    elapsed_time = time.time() - start_time

    # Crear diccionario de resultados
    results = {
        'sorted_counts': sorted_counts,
        'blank_count': blank_count,
        'total_words': len(words),
        'filename': get_filename_without_extension(filepath),
        'elapsed_time': elapsed_time
    }

    # Imprimir resultados en consola
    print_results(results)

    # Escribir resultados al archivo
    output_path = "WordCountResults.txt"
    write_results(results, output_path)

    print(f"Resultados guardados en: {output_path}")


if __name__ == "__main__":
    main()
