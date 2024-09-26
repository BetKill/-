from collections import defaultdict
import csv

def parse_csv(csv_str: str):
    """Парсинг CSV строки в списки родителей и детей."""
    children, parents = defaultdict(list), defaultdict(list)
    reader = csv.reader(csv_str.splitlines(), delimiter=',')
    for line in reader:
        if not line:
            continue
        parent, child = line
        children[parent].append(child)
        parents[child].append(parent)
        parents.setdefault(parent, [])
        children.setdefault(child, [])
    return children, parents

def find_root_and_leaves(parents, children):
    """Нахождение корня и листьев графа."""
    root = next(key for key in parents if not parents[key])
    leaves = [key for key in children if not children[key]]
    return root, leaves

def compute_relations(children, parents, root, leaves):
    """Вычисление всех пяти типов отношений для каждого узла."""
    certain_ans = {key: {'r1': set(children[key]),
                         'r2': set(parents[key]),
                         'r3': set(),
                         'r4': set(),
                         'r5': set()}
                   for key in parents}

    # Обход в глубину от корня для r4 и r5
    stack = [root]
    while stack:
        cur_node = stack.pop()
        for child in children[cur_node]:
            certain_ans[child]['r4'].update(certain_ans[cur_node]['r2'], certain_ans[cur_node]['r4'])
            certain_ans[child]['r5'].update(certain_ans[cur_node]['r1'] - {child})
            stack.append(child)

    # Обход вверх от листьев для r3
    stack = list(leaves)
    while stack:
        cur_node = stack.pop()
        for parent in parents[cur_node]:
            certain_ans[parent]['r3'].update(certain_ans[cur_node]['r1'], certain_ans[cur_node]['r3'])
            if parent not in stack:
                stack.append(parent)

    return certain_ans

def format_output(certain_ans):
    """Форматирование результата в CSV строку."""
    fields = ('r1', 'r2', 'r3', 'r4', 'r5')
    return '\n'.join([','.join(str(len(certain_ans[node][field])) for field in fields)
                      for node in sorted(certain_ans)]) + '\n'

def task(csv_str: str):
    """Основная функция для выполнения задачи."""
    children, parents = parse_csv(csv_str)
    root, leaves = find_root_and_leaves(parents, children)
    certain_ans = compute_relations(children, parents, root, leaves)
    return format_output(certain_ans)

if __name__ == '__main__':
    # Пример использования функции
    input_data = "1,2\n1,3\n3,4\n3,5\n"
    print(task(input_data))
