import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def task(temp_json, heating_json, rules_json, current_temp):
    # Парсинг JSON-строк
    temp_data = json.loads(temp_json)
    heating_data = json.loads(heating_json)
    rules_data = json.loads(rules_json)

    # Создание лингвистической переменной температуры
    temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
    for term in temp_data['температура']:
        points = [p[0] for p in term['points']]
        if len(points) == 4:
            temperature[term['id']] = fuzz.trapmf(temperature.universe, points)
        else:
            raise ValueError(f"Term '{term['id']}' must have exactly 4 points")

    # Создание лингвистической переменной уровня нагрева
    heating = ctrl.Consequent(np.arange(0, 11, 1), 'heating')
    for term in heating_data['уровень нагрева']:
        points = [p[0] for p in term['points']]
        if len(points) == 4:
            heating[term['id']] = fuzz.trapmf(heating.universe, points)
        else:
            raise ValueError(f"Term '{term['id']}' must have exactly 4 points")

    # Создание правил управления
    rules = []
    for rule in rules_data['управление']:
        antecedent = temperature[rule['if']]
        consequent = heating[rule['then']]
        rules.append(ctrl.Rule(antecedent, consequent))

    # Создание и симуляция системы управления
    heating_ctrl = ctrl.ControlSystem(rules)
    heating_simulation = ctrl.ControlSystemSimulation(heating_ctrl)

    # Установка текущей температуры и вычисление нагрева
    heating_simulation.input['temperature'] = current_temp
    heating_simulation.compute()

    # Возвращение значения оптимального управления
    return heating_simulation.output['heating']

# Пример использования функции
if __name__ == "__main__":
    temp_json = '''{
        "температура": [
            {"id": "холодно", "points": [[0, 1], [18, 1], [22, 0], [50, 0]]},
            {"id": "комфортно", "points": [[18, 0], [22, 1], [24, 1], [26, 0]]},
            {"id": "жарко", "points": [[0, 0], [24, 0], [26, 1], [50, 1]]}
        ]
    }'''

    heating_json = '''{
        "уровень нагрева": [
            {"id": "слабый", "points": [[0, 0], [4, 1], [6, 1], [10, 0]]},
            {"id": "умеренный", "points": [[0, 0], [4, 0], [6, 1], [8, 1]]},
            {"id": "интенсивный", "points": [[0, 0], [6, 0], [8, 1], [10, 1]]}
        ]
    }'''

    rules_json = '''{
        "управление": [
            {"if": "холодно", "then": "интенсивный"},
            {"if": "комфортно", "then": "умеренный"},
            {"if": "жарко", "then": "слабый"}
        ]
    }'''

    current_temp = 20.0
    heating_level = task(temp_json, heating_json, rules_json, current_temp)
    print(f'Temperature: {current_temp}°C, Heating level: {heating_level}')
