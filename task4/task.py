import argparse
import csv
import math


def load_csv_data(file_path: str):
    """Загрузка данных из CSV файла."""
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = list(reader)
    return [row[1:] for row in data[1:]]  # Пропускаем заголовки и первую колонку


def compute_joint_entropy(data):
    """Вычисление совместной энтропии."""
    entropy = 0
    for row in data:
        for value in row:
            if value > 0:
                entropy += value * math.log2(value)
    return round(-entropy, 2)


def compute_column_entropy(data):
    """Вычисление энтропии по столбцам."""
    column_totals = [0] * len(data[0])
    for row in data:
        for idx in range(len(row)):
            column_totals[idx] += row[idx]
    entropy = 0
    for total in column_totals:
        if total > 0:
            entropy += total * math.log2(total)
    return round(-entropy, 2), column_totals


def compute_row_entropy(data):
    """Вычисление энтропии по строкам."""
    entropy = 0
    row_totals = []
    for row in data:
        row_sum = sum(row)
        row_totals.append(row_sum)
        if row_sum > 0:
            entropy += row_sum * math.log2(row_sum)
    return round(-entropy, 2), row_totals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help="Путь к CSV файлу")
    args = parser.parse_args()

    # Загрузка данных и преобразование в числа
    matrix = load_csv_data(args.filepath)
    numeric_matrix = [[int(value) for value in row] for row in matrix]
    total_sum = sum(sum(row) for row in numeric_matrix)

    # Нормализация данных
    for i, row in enumerate(numeric_matrix):
        numeric_matrix[i] = [value / total_sum for value in row]

    # Вычисление энтропий
    joint_entropy_value = compute_joint_entropy(numeric_matrix)
    row_entropy, row_totals = compute_row_entropy(numeric_matrix)
    column_entropy, column_totals = compute_column_entropy(numeric_matrix)

    # Рассчитываем дополнительные значения
    mutual_entropy = joint_entropy_value - row_entropy
    information_b_given_a = column_entropy - mutual_entropy

    # Ответ
    results = [joint_entropy_value, row_entropy, column_entropy, mutual_entropy, information_b_given_a]
    return [round(result, 2) for result in results]


if __name__ == '__main__':
    print(main())
