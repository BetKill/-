import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def task(temp_mf_json, heat_mf_json, rules_json, current_temp):
    """
    Вычисление оптимального значения управления на основе нечеткой логики.

    Параметры:
        temp_mf_json (str): JSON-строка с описанием функций принадлежности для температуры.
        heat_mf_json (str): JSON-строка с описанием функций принадлежности для уровня нагрева.
        rules_json (str): JSON-строка с логическими правилами управления.
        current_temp (float): Текущее значение температуры (градусы Цельсия).

    Возвращает:
        float: Оптимальное значение управления.
    """
    # Парсинг JSON-строк в словари Python
    temp_mfs = json.loads(temp_mf_json)
    heat_mfs = json.loads(heat_mf_json)
    rules = json.loads(rules_json)

    # Определение универсумов для переменных
    min_temp = min(point[0] for mf in temp_mfs["температура"] for point in mf["points"])
    max_temp = max(point[0] for mf in temp_mfs["температура"] for point in mf["points"])
    min_heat = min(point[0] for mf in heat_mfs["уровень нагрева"] for point in mf["points"])
    max_heat = max(point[0] for mf in heat_mfs["уровень нагрева"] for point in mf["points"])

    temperature = ctrl.Antecedent(np.arange(min_temp, max_temp + 1, 1), 'temperature')
    heating = ctrl.Consequent(np.arange(min_heat, max_heat + 0.1, 0.1), 'heating')

    # Добавление функций принадлежности для температуры
    for mf in temp_mfs['температура']:
        points = np.array(mf['points'])
        temperature[mf['id']] = fuzz.trapmf(temperature.universe, [points[0][0], points[1][0],
                                                                   points[2][0], points[3][0]])

    # Добавление функций принадлежности для уровня нагрева
    for mf in heat_mfs['уровень нагрева']:
        points = np.array(mf['points'])
        heating[mf['id']] = fuzz.trapmf(heating.universe, [points[0][0], points[1][0], points[2][0], points[3][0]])

    # Создание правил логического вывода
    rule_list = []
    for rule in rules:
        if rule[0] in temperature.terms and rule[1] in heating.terms:
            rule_list.append(ctrl.Rule(temperature[rule[0]], heating[rule[1]]))

    # Создание и симуляция системы управления
    heating_ctrl = ctrl.ControlSystem(rule_list)
    heating_sim = ctrl.ControlSystemSimulation(heating_ctrl)

    # Ввод текущего значения температуры
    heating_sim.input['temperature'] = current_temp

    # Вычисление выходного значения
    heating_sim.compute()

    return heating_sim.output['heating']


# Пример JSON-данных для тестирования
if __name__ == "__main__":
    temp_mf_json = json.dumps({
        "температура": [
            {"id": "холодно", "points": [[0, 1], [18, 1], [22, 0], [50, 0]]},
            {"id": "комфортно", "points": [[18, 0], [22, 1], [24, 1], [26, 0]]},
            {"id": "жарко", "points": [[24, 0], [26, 1], [50, 1], [50, 0]]}
        ]
    })

    heat_mf_json = json.dumps({
        "уровень нагрева": [
            {"id": "слабый", "points": [[0, 0], [0, 1], [5, 1], [8, 0]]},
            {"id": "умеренный", "points": [[5, 0], [8, 1], [13, 1], [16, 0]]},
            {"id": "интенсивный", "points": [[13, 0], [18, 1], [23, 1], [26, 0]]}
        ]
    })

    rules_json = json.dumps([
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ])

    current_temp = 20

    # Запуск функции task
    optimal_heating = task(temp_mf_json, heat_mf_json, rules_json, current_temp)
    print(f"Оптимальный уровень нагрева: {optimal_heating:.2f}")
