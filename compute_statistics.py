#!/usr/bin/env python3
"""
computeStatistics.py - Calcula estadisticas descriptivas de un archivo.

Este programa lee un archivo con un numero por linea y calcula:
- Cuenta, Media, Mediana, Moda, Desviacion Estandar y Varianza

Uso: python compute_statistics.py archivoConDatos.txt

TC4017 - Calidad de Software
Tecnologico de Monterrey
"""

import sys
import time


def sqrt_manual(value):
    """
    Calculate square root using the Babylonian/Newton-Raphson method.

    Args:
        value: Non-negative number

    Returns:
        Square root of value, or None if value is negative
    """
    if value < 0:
        return None
    if value == 0:
        return 0.0

    guess = value / 2.0
    for _ in range(100):
        new_guess = (guess + value / guess) / 2.0
        if abs(new_guess - guess) < 1e-15:
            break
        guess = new_guess
    return guess


def sort_numbers(numbers):
    """
    Sort a list of numbers using merge sort algorithm.

    Args:
        numbers: List of numbers to sort

    Returns:
        New sorted list
    """
    if len(numbers) <= 1:
        return numbers[:]

    mid = len(numbers) // 2
    left = sort_numbers(numbers[:mid])
    right = sort_numbers(numbers[mid:])

    return merge(left, right)


def merge(left, right):
    """
    Merge two sorted lists into one sorted list.

    Args:
        left: First sorted list
        right: Second sorted list

    Returns:
        Merged sorted list
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def convert_to_number(num_str):
    """
    Convert string to int or float, preserving precision for large integers.

    Numbers ending in .0, .00, etc. are converted to int for precision.

    Args:
        num_str: String representation of a number

    Returns:
        int or float
    """
    if "." in num_str:
        # Check if decimal part is all zeros
        dot_pos = num_str.find(".")
        int_part = num_str[:dot_pos]
        dec_part = num_str[dot_pos + 1:]

        # If decimal part is all zeros, return as int
        all_zeros = True
        for char in dec_part:
            if char != "0":
                all_zeros = False
                break

        if all_zeros and int_part:
            if int_part == "-":
                return 0
            return int(int_part)
        return float(num_str)
    return int(num_str)


def extract_number(text):
    """
    Extract a number from text, handling trailing non-numeric characters.

    Accepts numbers with trailing letters (e.g., "405s" -> 405).
    Rejects numbers with non-numeric characters followed by more digits
    (e.g., "23,45" is invalid, not 23).

    Args:
        text: String potentially containing a number

    Returns:
        Tuple (number, success) where number is int/float and success is bool
    """
    text = text.strip()
    if not text:
        return None, False

    # Try direct conversion first
    result = _try_direct_conversion(text)
    if result[1]:
        return result

    # Try to extract number from start of string
    return _extract_partial_number(text)


def _try_direct_conversion(text):
    """Try to convert text directly to a number."""
    try:
        if "." in text:
            return convert_to_number(text), True
        return int(text), True
    except ValueError:
        return None, False


def _extract_partial_number(text):
    """Extract a number from the start of text, handling trailing chars."""
    num_chars = ""
    has_dot = False
    remaining = ""

    for idx, char in enumerate(text):
        if char == "-" and idx == 0:
            num_chars += char
        elif char == "." and not has_dot:
            has_dot = True
            num_chars += char
        elif char in "0123456789":
            num_chars += char
        else:
            remaining = text[idx:]
            break

    if not num_chars or num_chars in ("-", "."):
        return None, False

    # Check if remaining text contains any digits (reject if so)
    if any(char in "0123456789" for char in remaining):
        return None, False

    try:
        return convert_to_number(num_chars), True
    except ValueError:
        return None, False


def read_numbers_from_file(filepath):
    """
    Read numbers from a file, one per line.

    Args:
        filepath: Path to the input file

    Returns:
        Tuple (valid_numbers, total_count) where valid_numbers is list of
        successfully parsed numbers and total_count includes invalid data
    """
    numbers = []
    total_count = 0

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue

                total_count += 1
                num, success = extract_number(line)
                if success:
                    numbers.append(num)
                else:
                    print(f"Error: Dato invalido en la linea {
                          line_num}: " f'"{line}"')

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {filepath}")
        sys.exit(1)
    except IOError as io_error:
        print(f"Error: No se pudo leer el archivo: {io_error}")
        sys.exit(1)

    return numbers, total_count


def calculate_mean(numbers):
    """
    Calculate the arithmetic mean.

    Args:
        numbers: List of numbers

    Returns:
        Mean value
    """
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)


def calculate_median(numbers):
    """
    Calculate the median value.

    For large integers, preserves precision by using integer division
    when possible.

    Args:
        numbers: List of numbers (will be sorted internally)

    Returns:
        Median value
    """
    sorted_nums = sort_numbers(numbers)
    length = len(sorted_nums)

    if length % 2 == 1:
        return sorted_nums[length // 2]

    mid = length // 2
    val1 = sorted_nums[mid - 1]
    val2 = sorted_nums[mid]
    total = val1 + val2

    # If both are integers and sum is even, use integer division
    if isinstance(val1, int) and isinstance(val2, int):
        if total % 2 == 0:
            return total // 2
        # Result will be .5, but keep precision for integer part
        return total / 2
    return total / 2


def calculate_mode(numbers):
    """
    Calculate the mode (most frequent value).

    When there are multiple modes (tie), returns the one that appeared first.

    Args:
        numbers: List of numbers

    Returns:
        Mode value, or "#N/A" if all values appear only once
    """
    frequency = {}
    first_occurrence = {}

    for idx, num in enumerate(numbers):
        if num in frequency:
            frequency[num] = frequency[num] + 1
        else:
            frequency[num] = 1
            first_occurrence[num] = idx

    max_count = 0
    for count in frequency.values():
        if count > max_count:
            max_count = count

    if max_count == 1:
        return "#N/A"

    # Find all modes and select the one that appeared first
    best_mode = None
    best_first_idx = float("inf")

    for value, count in frequency.items():
        if count == max_count:
            if first_occurrence[value] < best_first_idx:
                best_first_idx = first_occurrence[value]
                best_mode = value

    return best_mode


def calculate_sum_squared_diff(numbers, mean):
    """
    Calculate sum of squared differences from mean.

    Args:
        numbers: List of numbers
        mean: Pre-calculated mean value

    Returns:
        Sum of (xi - mean)^2
    """
    total = 0
    for num in numbers:
        diff = num - mean
        total = total + (diff * diff)
    return total


def calculate_sample_variance(numbers, mean):
    """
    Calculate the sample variance (for reporting).

    Args:
        numbers: List of numbers
        mean: Pre-calculated mean value

    Returns:
        Sample variance (using n-1 denominator)
    """
    sum_sq = calculate_sum_squared_diff(numbers, mean)
    return sum_sq / (len(numbers) - 1)


def calculate_population_std_dev(numbers, mean):
    """
    Calculate the population standard deviation.

    Args:
        numbers: List of numbers
        mean: Pre-calculated mean value

    Returns:
        Population standard deviation (using n denominator)
    """
    sum_sq = calculate_sum_squared_diff(numbers, mean)
    pop_variance = sum_sq / len(numbers)
    return sqrt_manual(pop_variance)


def format_number(value):
    """
    Format a number for output display.

    Args:
        value: Number to format

    Returns:
        Formatted string representation
    """
    if isinstance(value, str):
        return value

    if isinstance(value, int):
        return str(value)

    if value == int(value):
        return str(int(value))

    return str(value)


def get_filename(filepath):
    """
    Extract filename from a filepath.

    Args:
        filepath: Full path or relative path to file

    Returns:
        Just the filename without directory path
    """
    # Find last separator (/ or \)
    last_sep = -1
    for idx, char in enumerate(filepath):
        if char in ('/', '\\'):
            last_sep = idx

    if last_sep == -1:
        return filepath
    return filepath[last_sep + 1:]


def read_existing_results(output_file):
    """
    Read existing results file and parse into data structure.

    Args:
        output_file: Path to the results file

    Returns:
        Tuple (labels, columns) where labels is list of row labels
        and columns is dict mapping filename to list of values
    """
    labels = []
    columns = {}
    header_row = []

    try:
        with open(output_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if len(lines) == 0:
            return labels, columns

        # Parse header row to get column names (use rstrip to preserve tabs)
        header_parts = lines[0].rstrip("\n").split("\t")
        if len(header_parts) > 1:
            header_row = header_parts[1:]  # Skip first column (empty)

        # Initialize columns dict
        for col_name in header_row:
            columns[col_name] = []

        # Parse data rows
        for line in lines[1:]:
            parts = line.rstrip("\n").split("\t")
            if len(parts) > 0:
                labels.append(parts[0])
                for i, col_name in enumerate(header_row):
                    if i + 1 < len(parts):
                        columns[col_name].append(parts[i + 1])
                    else:
                        columns[col_name].append("")

    except FileNotFoundError:
        pass
    except IOError:
        pass

    return labels, columns


def _get_row_labels():
    """Return the standard row labels for statistics output."""
    return ["CUENTA", "MEDIA", "MEDIANA", "MODA", "DESV EST", "VARIANZA", "TIEMPO"]


def _format_stats_values(stats, elapsed_time):
    """Format statistics values for output."""
    return [
        format_number(stats["count"]),
        format_number(stats["mean"]),
        format_number(stats["median"]),
        format_number(stats["mode"]),
        format_number(stats["sd"]),
        format_number(stats["variance"]),
        f"{elapsed_time:.3f}s",
    ]


def _write_table_to_file(output_file, labels, columns):
    """Write the statistics table to file."""
    col_names = list(columns.keys())
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\t" + "\t".join(col_names) + "\n")
            for i, label in enumerate(labels):
                row_values = [
                    columns[col][i] if i < len(columns[col]) else ""
                    for col in col_names
                ]
                file.write(label + "\t" + "\t".join(row_values) + "\n")
    except IOError as io_error:
        print(f"Error: No se pudo escribir el archivo de resultados: {io_error}")


def write_results(stats, elapsed_time, input_filename):
    """
    Write results to StatisticsResults.txt file in tabular format.

    If file exists, adds a new column with the results.
    Column is named after the input filename.

    Args:
        stats: Dictionary with computed statistics
        elapsed_time: Time elapsed for computation
        input_filename: Name of the input file (used as column header)
    """
    output_file = "StatisticsResults.txt"
    col_name = get_filename(input_filename).replace(".txt", "")

    existing_labels, existing_columns = read_existing_results(output_file)

    if len(existing_labels) == 0:
        existing_labels = _get_row_labels()

    existing_columns[col_name] = _format_stats_values(stats, elapsed_time)
    _write_table_to_file(output_file, existing_labels, existing_columns)


def print_results(stats, elapsed_time):
    """
    Print results to console.

    Args:
        stats: Dictionary with computed statistics
        elapsed_time: Time elapsed for computation
    """
    print(f"CUENTA: {format_number(stats['count'])}")
    print(f"MEDIA: {format_number(stats['mean'])}")
    print(f"MEDIANA: {format_number(stats['median'])}")
    print(f"MODA: {format_number(stats['mode'])}")
    print(f"DESV EST: {format_number(stats['sd'])}")
    print(f"VARIANZA: {format_number(stats['variance'])}")
    print(f"Tiempo transcurrido: {elapsed_time:.3f} segundos")


def main():
    """Main function to orchestrate the statistics computation."""
    if len(sys.argv) != 2:
        print("Uso: python compute_statistics.py archivoConDatos.txt")
        sys.exit(1)

    filepath = sys.argv[1]

    start_time = time.time()

    numbers, total_count = read_numbers_from_file(filepath)

    if len(numbers) == 0:
        print("Error: No se encontraron numeros validos en el archivo")
        sys.exit(1)

    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    variance = calculate_sample_variance(numbers, mean)
    std_dev = calculate_population_std_dev(numbers, mean)

    elapsed_time = time.time() - start_time

    stats = {
        "count": total_count,
        "mean": mean,
        "median": median,
        "mode": mode,
        "sd": std_dev,
        "variance": variance,
    }

    print_results(stats, elapsed_time)
    write_results(stats, elapsed_time, filepath)


if __name__ == "__main__":
    main()
