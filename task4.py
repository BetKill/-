from collections import defaultdict
from functools import reduce
from math import log2


def calculate_counts():
    counts_ab, counts_a, counts_b = defaultdict(int), defaultdict(int), defaultdict(int)
    for i in range(1, 7):
        for j in range(1, 7):
            sum_val, prod_val = i + j, i * j
            counts_ab[(sum_val, prod_val)] += 1
            counts_a[sum_val] += 1
            counts_b[prod_val] += 1
    return counts_ab, counts_a, counts_b


def calculate_probability(mass: defaultdict) -> dict:
    return {key: (value / 36) for key, value in mass.items()}


def calculate_entropy(mass: dict) -> float:
    return reduce(lambda e, prob: e - prob * log2(prob), mass.values(), 0)


def round_values(entropies: [float]) -> [float]:
    return [round(e, 2) for e in entropies]


def task() -> list:
    counts_ab, counts_a, counts_b = calculate_counts()
    probability_ab = calculate_probability(counts_ab)
    probability_a = calculate_probability(counts_a)
    probability_b = calculate_probability(counts_b)

    entropy_ab = calculate_entropy(probability_ab)
    entropy_a = calculate_entropy(probability_a)
    entropy_b = calculate_entropy(probability_b)

    entropy_b_given_a = entropy_ab - entropy_a
    information_a_about_b = entropy_b - entropy_b_given_a

    return round_values([entropy_ab, entropy_a, entropy_b, entropy_b_given_a, information_a_about_b])

if __name__ == '__main__':
    print(task())
