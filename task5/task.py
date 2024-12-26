import json
import numpy as np


def get_matrix(str_json: str):
    clusters = [c if isinstance(c, list) else [c] for c in json.loads(str_json)]
    n = sum(len(cluster) for cluster in clusters)

    matrix = np.ones((n, n), dtype=int)

    worse = []
    for cluster in clusters:
        for worse_elem in worse:
            for elem in cluster:
                matrix[elem - 1][worse_elem - 1] = 0
        for elem in cluster:
            worse.append(int(elem))

    return matrix


def get_clusters(matrix, est1, est2):
    clusters = {}
    num_rows = len(matrix)

    excluded_rows = set()
    for row in range(num_rows):
        if row + 1 in excluded_rows:
            continue
        current_cluster = [row + 1]
        clusters[row + 1] = current_cluster
        for col in range(row + 1, num_rows):
            if matrix[row][col] == 0:
                current_cluster.append(col + 1)
                excluded_rows.add(col + 1)

    result = []

    for k in clusters:
        current_cluster = clusters[k]
        sum_est1_elem = np.sum(est1[current_cluster[0] - 1])
        sum_est2_elem = np.sum(est2[current_cluster[0] - 1])

        # Прямое добавление в результат
        result.append(current_cluster)

    return result


def task(string1, string2):
    matrix1 = get_matrix(string1)
    matrix2 = get_matrix(string2)

    matrix_and = np.multiply(matrix1, matrix2)
    matrix_and_t = np.multiply(np.transpose(matrix1), np.transpose(matrix2))

    matrix_or = np.maximum(matrix_and, matrix_and_t)

    # Эмуляция оценок, поскольку они не переданы в строках JSON
    est1 = np.random.rand(matrix_or.shape[0], matrix_or.shape[0])  # Пример случайных оценок
    est2 = np.random.rand(matrix_or.shape[0], matrix_or.shape[0])  # Пример случайных оценок

    clusters = get_clusters(matrix_or, est1, est2)

    return clusters


if __name__ == "__main__":
    string1 = '[1,[2,3],4,[5,6,7],8,9,10]'
    string2 = '[[1,2],[3,4,5],6,7,9,[8,10]]'
    results = task(string1, string2)
    print(results)
