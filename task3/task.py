import argparse
import csv
import math


def load_csv_file() -> list[list[str]]:
    """Чтение CSV файла и преобразование в список строк."""
    parser = argparse.ArgumentParser(description="CSV file entropy calculator")
    parser.add_argument('file_path', help="Путь к файлу CSV")
    args = parser.parse_args()
    with open(args.file_path, mode='r') as file:
        data = list(csv.reader(file, delimiter=','))
    return data


def compute_entropy(data: list[list[str]]) -> float:
    """Вычисление энтропии для данных в CSV."""
    entropy = 0
    total_rows = len(data)

    for row in data:
        for value in row:
            if value != '0':
                probability = float(value) / (total_rows - 1)
                entropy += -probability * math.log2(probability)

    return round(entropy, 1)


def execute_task():
    """Основная функция для выполнения задачи."""
    csv_data = load_csv_file()
    result = compute_entropy(csv_data)
    print(result)


if __name__ == '__main__':
    execute_task()
