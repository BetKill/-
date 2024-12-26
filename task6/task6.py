import argparse
import json
import numpy as np
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def task(temp_mf_json, heat_mf_json, rules_json, current_temp):
    # Загрузка функций принадлежности и правил
    temp_mfs = json.loads(temp_mf_json)
    heat_mfs = json.loads(heat_mf_json)
    rules = json.loads(rules_json)

    # Инициализация минимальных и максимальных значений
    min_temp = float('inf')
    max_temp = float('-inf')
    min_heat = float('inf')
    max_heat = float('-inf')

    # Определение диапазона температур
    for state in temp_mfs["температура"]:
        points = state["points"]
        for point in points:
            temperature = point[0]
            min_temp = min(min_temp, temperature)
            max_temp = max(max_temp, temperature)

    # Определение диапазона уровней нагрева
    for state in heat_mfs["уровень нагрева"]:
        points = state["points"]
        for point in points:
            heat = point[0]
            min_heat = min(min_heat, heat)
            max_heat = max(max_heat, heat)

    # Создание входных и выходных переменных
    temperature = ctrl.Antecedent(np.arange(min_temp, max_temp, 1), 'temperature')
    heating = ctrl.Consequent(np.arange(min_heat, max_heat, 0.1), 'heating')

    # Определение функций принадлежности для температуры
    for mf in temp_mfs['температура']:
        points = np.array(mf['points'])
        temperature[mf['id']] = fuzz.trapmf(temperature.universe, [points[0][0], points[1][0], points[2][0], points[3][0]])

    # Определение функций принадлежности для уровня нагрева
    for mf in heat_mfs['уровень нагрева']:
        points = np.array(mf['points'])
        heating[mf['id']] = fuzz.trapmf(heating.universe, [points[0][0], points[1][0], points[2][0], points[3][0]])

    # Активированные правила
    activated_rules = []
    for rule in rules:
        if rule[0] in temperature.terms and rule[1] in heating.terms:
            temp_level = fuzz.interp_membership(temperature.universe, temperature[rule[0]].mf, current_temp)
            if temp_level > 0:
                activated_rules.append((temp_level, rule[1]))

    # Композиция активированных правил
    output_mf = np.zeros_like(heating.universe)
    for activation_level, heat_term in activated_rules:
        heat_mf = heating[heat_term].mf
        output_mf = np.maximum(output_mf, np.minimum(activation_level, heat_mf))

    # Дефаззификация
    if np.any(output_mf):
        defuzzified_output = fuzz.defuzz(heating.universe, output_mf, 'centroid')
        return defuzzified_output
    else:
        raise ValueError("Выходная область пуста")


def load_json(source, default):
    try:
        if os.path.isfile(source):
            with open(source, 'r') as file:
                return json.load(file)
        return json.loads(source)
    except Exception:
        return default


if __name__ == "__main__":
    # Значения по умолчанию
    default_temp_mf = {
        "температура": [
            {"id": "холодно", "points": [[0, 0], [5, 1], [10, 1], [12, 0]]},
            {"id": "комфортно", "points": [[18, 0], [22, 1], [24, 1], [26, 0]]},
            {"id": "жарко", "points": [[0, 0], [24, 0], [26, 1], [40, 1], [50, 0]]}
        ]
    }

    default_heat_mf = {
        "уровень нагрева": [
            {"id": "слабый", "points": [[0, 0], [0, 1], [5, 1], [8, 0]]},
            {"id": "умеренный", "points": [[5, 0], [8, 1], [13, 1], [16, 0]]},
            {"id": "интенсивный", "points": [[13, 0], [18, 1], [23, 1], [26, 0]]}
        ]
    }

    default_rules = [
        ['холодно', 'интенсивный'],
        ['комфортно', 'умеренный'],
        ['жарко', 'слабый']
    ]

    default_current_temp = 15

    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('--temp_file', type=str, help='Путь к файлу с функциями принадлежности температуры')
    parser.add_argument('--heat_file', type=str, help='Путь к файлу с функциями принадлежности уровня нагрева')
    parser.add_argument('--rules_file', type=str, help='Путь к файлу с правилами')
    parser.add_argument('--current_temp', type=int, default=default_current_temp, help='Текущая температура')
    args = parser.parse_args()

    # Загрузка данных из файлов или использование значений по умолчанию
    temp_mf_json = load_json(args.temp_file, json.dumps(default_temp_mf))
    heat_mf_json = load_json(args.heat_file, json.dumps(default_heat_mf))
    rules_json = load_json(args.rules_file, json.dumps(default_rules))
    current_temp = args.current_temp

    try:
        # Выполнение задачи
        optimal_heating = task(temp_mf_json, heat_mf_json, rules_json, current_temp)
        print(f"{optimal_heating:.2f}")
    except ValueError as e:
        print(f"Ошибка: {e}")
