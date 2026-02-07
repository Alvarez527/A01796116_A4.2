"""
Programa para convertir números enteros a binario y hexadecimal.

Actividad 4.2 - TC4017 Calidad de Software
Tecnológico de Monterrey

Uso: python convert_numbers.py archivoConDatos.txt
"""

import sys
import time
import os


def int_to_binary(number):
    """
    Convierte un entero positivo a su representación binaria.

    Args:
        number: Número entero positivo

    Returns:
        String con la representación binaria
    """
    if number == 0:
        return "0"
    bits = ""
    while number > 0:
        bits = str(number % 2) + bits
        number = number // 2
    return bits


def int_to_hex(number):
    """
    Convierte un entero positivo a su representación hexadecimal.

    Args:
        number: Número entero positivo

    Returns:
        String con la representación hexadecimal (mayúsculas)
    """
    if number == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    result = ""
    while number > 0:
        result = hex_chars[number % 16] + result
        number = number // 16
    return result


def convert_number(number):
    """
    Convierte un número a binario y hexadecimal.

    Para números negativos usa complemento a 2:
    - Binario: últimos 10 bits
    - Hexadecimal: FFFFFFFF + últimos 2 dígitos hex

    Args:
        number: Número entero

    Returns:
        Tupla (binary, hex) con las representaciones
    """
    if number >= 0:
        return int_to_binary(number), int_to_hex(number)

    # Complemento a 2 para números negativos
    complement_32 = (1 << 32) + number

    # Hexadecimal: FFFFFFFF + últimos 2 dígitos (formato especial)
    hex_full = int_to_hex(complement_32)
    # Tomar solo los últimos 2 caracteres y anteponer FFFFFFFF
    last_two_hex = hex_full[-2:] if len(hex_full) >= 2 else hex_full
    hex_result = "FFFFFFFF" + last_two_hex

    # 10 bits para binario (últimos 10 bits del complemento)
    binary_full = int_to_binary(complement_32)
    binary_result = binary_full[-10:] if len(binary_full) >= 10 else binary_full

    return binary_result, hex_result


def read_numbers_from_file(filepath):
    """
    Lee números de un archivo de texto.

    Args:
        filepath: Ruta al archivo

    Returns:
        Lista de tuplas (valor_original, numero_o_none, es_valido)
    """
    numbers = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                num = int(line)
                numbers.append((line, num, True))
            except ValueError:
                numbers.append((line, None, False))
    return numbers


def get_filename_without_extension(filepath):
    """Extrae el nombre del archivo sin extensión."""
    basename = os.path.basename(filepath)
    name, _ = os.path.splitext(basename)
    return name


def print_results(data, filename, elapsed_time):
    """
    Imprime los resultados en consola.

    Args:
        data: Lista de tuplas (valor, binary, hex)
        filename: Nombre del archivo procesado
        elapsed_time: Tiempo de ejecución en segundos
    """
    print(f"\t{filename}\tBIN\tHEX")
    print("ITEM")
    for i, (value, binary, hexval) in enumerate(data, 1):
        print(f"{i}\t{value}\t{binary}\t{hexval}")
    print(f"TIEMPO\t{elapsed_time:.3f}s")


def write_results(data, filename, elapsed_time, output_path):
    """
    Escribe los resultados al archivo de salida.

    Si el archivo existe, agrega los nuevos resultados debajo.
    Si no existe, crea el archivo con el formato inicial.

    Args:
        data: Lista de tuplas (valor, binary, hex)
        filename: Nombre del archivo procesado
        elapsed_time: Tiempo de ejecución en segundos
        output_path: Ruta del archivo de salida
    """
    # Preparar las líneas de este resultado
    result_lines = []
    result_lines.append(f"ITEM\t{filename}\tBIN\tHEX\n")
    for i, (value, binary, hexval) in enumerate(data, 1):
        result_lines.append(f"{i}\t{value}\t{binary}\t{hexval}\n")
    result_lines.append(f"TIEMPO\t{elapsed_time:.3f}s\n")

    if os.path.exists(output_path):
        # Agregar resultados debajo del contenido existente
        with open(output_path, 'a', encoding='utf-8') as file:
            file.write("\n\n")  # Líneas en blanco para separar
            file.writelines(result_lines)
    else:
        # Crear archivo nuevo
        with open(output_path, 'w', encoding='utf-8') as file:
            file.writelines(result_lines)


def _get_input_filepath():
    """Obtiene y valida la ruta del archivo de entrada."""
    if len(sys.argv) < 2:
        print("Uso: python convert_numbers.py archivoConDatos.txt")
        sys.exit(1)
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: Archivo no encontrado: {input_path}")
        sys.exit(1)
    return input_path


def main():
    """Función principal del programa."""
    filepath = _get_input_filepath()
    start_time = time.time()

    # Leer números del archivo
    numbers = read_numbers_from_file(filepath)

    # Convertir cada número
    results = []
    for i, (original, num, is_valid) in enumerate(numbers, 1):
        if is_valid:
            binary, hexval = convert_number(num)
            results.append((original, binary, hexval))
        else:
            print(f"Error: Dato inválido '{original}' en la línea {i}")
            results.append((original, "#VALUE!", "#VALUE!"))

    # Calcular tiempo transcurrido
    elapsed_time = time.time() - start_time

    # Obtener nombre del archivo sin extensión
    filename = get_filename_without_extension(filepath)

    # Imprimir resultados en consola
    print_results(results, filename, elapsed_time)

    # Escribir resultados al archivo
    output_path = "ConvertionResults.txt"
    write_results(results, filename, elapsed_time, output_path)

    print(f"\nResultados guardados en: {output_path}")
    print(f"Tiempo transcurrido: {elapsed_time:.3f} segundos")


if __name__ == "__main__":
    main()
