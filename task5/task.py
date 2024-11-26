import argparse
import json
import numpy as np


def get_matrix(str_json: str):
    clusters = [c if isinstance(c, list) else [c] for c in json.loads(str_json)]
    n = sum(len(cluster) for cluster in clusters)

    matrix = [[1] * n for _ in range(n)]

    worse = []
    for cluster in clusters:
        for worse_elem in worse:
            for elem in cluster:
                matrix[elem - 1][worse_elem - 1] = 0
        for elem in cluster:
            worse.append(int(elem))

    return np.array(matrix)

def get_clusters(matrix, est1, est2):
    clusters = {}

    num_rows = len(matrix)
    num_cols = len(matrix[0])
    excluded_rows = set()
    for row in range(num_rows):
        if row + 1 in excluded_rows:
            continue
        current_cluster = [row + 1]
        clusters[row + 1] = current_cluster
        for col in range(row + 1, num_cols):
            if matrix[row][col] == 0:
                current_cluster.append(col + 1)
                excluded_rows.add(col + 1)

    result = []
    for k in clusters:
        if not result:
            result.append(clusters[k])
            continue

        for i, elem in enumerate(result):
            sum_est1_elem = np.sum(est1[elem[0] - 1])
            sum_est2_elem = np.sum(est2[elem[0] - 1])
            sum_est1_k = np.sum(est1[k - 1])
            sum_est2_k = np.sum(est2[k - 1])

            if sum_est1_elem == sum_est1_k and sum_est2_elem == sum_est2_k:
                for c in clusters[k]:
                    result[i].append(c)
                    break
            if sum_est1_elem < sum_est1_k or sum_est2_elem < sum_est2_k:
                result = result[:i] + clusters[k] + result[i:]
                break

        result.append(clusters[k])

    final_result = [r[0] if len(r) == 1 else r for r in result]
    return str(final_result)


def task(string1:str , string2:str):
    matrix1 = get_matrix(string1)
    matrix2 = get_matrix(string2)

    matrix_and = np.multiply(matrix1, matrix2)
    matrix_and_t = np.multiply(np.transpose(matrix1), np.transpose(matrix2))

    matrix_or = np.maximum(matrix_and, matrix_and_t)
    clusters = get_clusters(matrix_or, matrix1, matrix2)
    return clusters

def find_sublists(array_str):
    array = json.loads(array_str)
    sublists = [element for element in array if isinstance(element, list)]
    return sublists


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", type=str)
    parser.add_argument("file2", type=str)
    args = parser.parse_args()
    with open(args.file1, "r") as f1:
        string1 = f1.read().strip()

    with open(args.file2, "r") as f2:
        string2 = f2.read().strip()

    clusters = task(string1, string2)
    results = find_sublists(clusters)
    print(results)