import csv
import sys

def get_csv_value(file_path, row_number, column_number):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            if row_number < 1 or row_number > len(rows):
                raise IndexError("Номер строки выходит за пределы.")
            if column_number < 1 or column_number > len(rows[0]):
                raise IndexError("Номер столбца выходит за пределы.")
            value = rows[row_number - 1][column_number - 1]
            if value != "":
                print(f"Значение в строке {row_number} и столбце {column_number}: {value}")
            else:
                print("Там пусто")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except IndexError as e:
        print(e)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python script.py <путь к файлу> <номер строки> <номер столбца>")
    else:
        file_path = sys.argv[1]
        row_number = int(sys.argv[2])
        column_number = int(sys.argv[3])
        get_csv_value(file_path, row_number, column_number)