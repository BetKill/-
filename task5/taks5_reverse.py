import json
import numpy as np


def get_matrix(filepath: str):
    """Преобразует JSON-файл с кластерами в матрицу предпочтений."""
    with open(filepath, 'r') as file:
        clusters = json.load(file)

    clusters = [c if isinstance(c, list) else [c] for c in clusters]
    n = sum(len(cluster) for cluster in clusters)

    matrix = [[1] * n for _ in range(n)]
    worse = []
    for cluster in clusters:
        for worse_element in worse:
            for element in cluster:
                matrix[element - 1][worse_element - 1] = 0
                # print(element-1, worse_element-1)
        for element in cluster:
            worse.append(int(element))

    return np.array(matrix)


def find_clusters(matrix):
    """Находит конфликтные пары элементов в матрице."""
    conflict_core = []

    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] == 0 and matrix[j][i] == 0:  # Если оба элемента противоречат друг другу
                conflict_pair = sorted([i + 1, j + 1])
                if conflict_pair not in conflict_core:
                    conflict_core.append(conflict_pair)

    final_result = [pair[0] if len(pair) == 1 else pair for pair in conflict_core]
    return str(final_result)


def main(file_path1: str, file_path2: str):
    """Основная функция для нахождения конфликтных кластеров из двух файлов."""
    matrix1 = get_matrix(file_path1)
    matrix2 = get_matrix(file_path2)

    # Создаем пересечение и объединение матриц
    matrix_and = np.multiply(matrix1, matrix2)
    matrix_and_t = np.multiply(np.transpose(matrix1), np.transpose(matrix2))
    matrix_or = np.maximum(matrix_and, matrix_and_t)

    clusters = find_clusters(matrix_or)
    return clusters


if __name__ == '__main__':
    print(main("example1.json", "example2.json"))