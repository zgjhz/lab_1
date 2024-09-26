import generic as g
from datetime import datetime
from time import time as t
person_num = 10
start_time = datetime.strptime("08:00", "%H:%M")
end_time = datetime.strptime("21:00", "%H:%M")

person_num = int(input(f"Введите колличество людей в датасете: "))

def get_distribution(entities, entity_type):
    """Функция для ввода распределения от пользователя для указанных сущностей."""
    distribution = {}
    print(f"\nВведите распределение для каждого {entity_type} в формате долей (например, 0.6 для 60%)")
    for entity in entities:
        while True:
            try:
                share = float(input(f"Введите долю для {entity}: "))
                if 0 <= share <= 1:
                    distribution[entity] = share
                    break
                else:
                    print("Ошибка: доля должна быть числом от 0 до 1.")
            except ValueError:
                print("Ошибка: введите число в виде десятичной дроби (например, 0.6).")

    total_share = sum(distribution.values())
    if total_share != 1.0:
        print(f"\nПредупреждение: сумма долей для {entity_type} не равна 1. Нормализуем пропорции...")
        for entity in distribution:
            distribution[entity] /= total_share

    print(f"\nРаспределение {entity_type}:")
    for entity, share in distribution.items():
        print(f"{entity}: {share:.2f}")

    return distribution

def get_bank_and_payment_distributions():
    """Функция для настройки распределений банков и платёжных систем."""
    banks = ['Сбербанк', 'Альфа-Банк', 'Тинькофф', 'ВТБ']
    payment_systems = ['Visa', 'MasterCard', 'Мир']

    bank_distribution = get_distribution(banks, "банков")
    payment_system_distribution = get_distribution(payment_systems, "платёжных систем")

    return bank_distribution, payment_system_distribution

bank_distribution, payment_system_distribution = get_bank_and_payment_distributions()

f = t()
persons = g.create_persons(person_num, start_time, end_time, bank_distribution, payment_system_distribution)
g.save_to_xml(persons, "dataset")
print(t() - f)
0.6
0.2
0.1
0.1
0.5
0.3
0.2