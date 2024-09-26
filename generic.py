import random
import data.full_names as full_names
import data.doctors as doctors
from datetime import datetime, timedelta
from faker import Faker
import json
import string
import xml.etree.ElementTree as ET

fake = Faker()

def generate_name():
    gender = random.randint(0, 1)
    if gender == 0:
        return random.choice(full_names.male_surnames) + " " + random.choice(full_names.male_names) + " " + random.choice(full_names.male_patronymics)
    else:
        return random.choice(full_names.female_surnames) + " " + random.choice(full_names.female_names) + " " + random.choice(full_names.female_patronymics)

class Identity:
    def __init__(self):
        self.country = random.choice(['Россия', 'Беларусь', 'Казахстан'])
        self.passport_data = self.generate_passport_data()
        self.snils = self.generate_snils()
        self.id = self.generate_unique_id()

    @staticmethod
    def generate_unique_id():
        return random.randint(100000, 999999)

    @staticmethod
    def generate_snils():
        return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)} {random.randint(10, 99)}"

    def generate_passport_data(self):
        country = self.country
        if country == 'Россия':
            series = random.randint(1000, 9999)
            numbers = random.randint(100000, 999999)
        if country == 'Беларусь':
            series = ''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = ''.join(random.choices(string.digits, k=7))
        if country == 'Казахстан':
            series = 'N'#''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = ''.join(random.choices(string.digits, k=7))
        return f"{series} {numbers}"
    
class Card:
    def __init__(self, bank, payment_system):
        self.bank = bank
        self.payment_system = payment_system
        self.card_number = self.generate_card_number()

    @staticmethod
    def generate_card_number():
        return f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"

class Visit:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.doctor = random.choice(list(doctors.doctor_symptoms.keys()))
        self.symptoms = self.generate_symptoms()
        self.date_of_visit = self.generate_date_of_visit()
        self.analysis = self.generate_analysis()
        self.date_of_analysis = self.generate_date_of_analysis()
        self.cost = self.generate_cost()

    def generate_symptoms(self):
        symptoms_data = doctors.doctor_symptoms[self.doctor]
        symptoms = random.sample(symptoms_data, random.randint(1, len(symptoms_data)))
        return ', '.join(symptoms)

    def generate_date_of_visit(self):
        date = fake.date_time_between(start_date='-2y', end_date='now')
        hour = date.hour
        date = date + timedelta(hours=random.randint(self.start_time.hour - hour, self.end_time.hour - hour))
        return date.strftime("%Y-%m-%dT%H:%M:%S+03:00")

    def generate_date_of_analysis(self):
        date_of_visit = datetime.strptime(self.date_of_visit, "%Y-%m-%dT%H:%M:%S+03:00")
        date_of_visit = date_of_visit + timedelta(hours=random.randint(24, 72), minutes=random.randint(1, 59), seconds=random.randint(1, 59))
        hour = date_of_visit.hour
        date_of_visit = date_of_visit + timedelta(hours=random.randint(self.start_time.hour - hour, self.end_time.hour - hour))
        return (date_of_visit).strftime("%Y-%m-%dT%H:%M:%S+03:00")

    def generate_analysis(self):
        analysis = random.sample(doctors.doctor_tests[self.doctor], random.randint(1, 3))
        return ', '.join(analysis)
    @staticmethod
    def generate_cost():
        return round(random.uniform(0.2, 1.2) * 10000)
    
class Person:
    def __init__(self, fio, card):
        self.fio = fio
        self.identity = Identity()
        self.card = card
        self.visits = []

    def add_visits(self, visits_num, start_time, end_time):
        for _ in range(visits_num):
            visit = Visit(start_time, end_time)
            self.visits.append(visit)

    def to_dict(self):
        json = {
            'ФИО': self.fio,
            'Страна': self.identity.country,
            'Паспортые данные': self.identity.passport_data,
            'СНИЛС': self.identity.snils,
            'Карта': {
                'Номер карты': self.card.card_number,
                'Банк': self.card.bank,
                'Платежная система': self.card.payment_system
            }
        }
        for i, visit in enumerate(self.visits, 1):
            json_visit = {
                f'Визит {i}': {
                    'Симптомы' : visit.symptoms,
                    'Врач':  visit.doctor,
                    'Дата посещения врача' : visit.date_of_visit,
                    'Анализы' : visit.analysis,
                    'Дата получения анализов' : visit.date_of_analysis,
                    'Цена приёма' : f'{visit.cost}руб.'
                } 
            }
            json.update(json_visit)
        return json

def create_persons(person_num, start_time, end_time, bank_distribution, payment_system_distribution):
    def generate_system(system_distribution):
        systems = []
        for system, count in system_distribution.items():
            count = count * person_num
            for _ in range(int(count)):
                systems.append(system)
        random.shuffle(systems)
        return systems

    def generate_cards(distribution):
        cards = []
        systems = generate_system(payment_system_distribution)
        for bank, count in distribution.items():
            count = count * person_num
            for _ in range(int(count)):
                system = systems.pop()
                card = Card(bank=bank, payment_system=system)
                cards.append(card)

        random.shuffle(cards)

        return cards
    
    persons = []
    cards = generate_cards(bank_distribution)
    for _ in range(person_num):
        fio = generate_name()
        card = cards.pop()
        person = Person(fio=fio, card=card)
        person.add_visits(random.randint(1, 5), start_time, end_time)
        persons.append(person)
    return persons

def save_to_json(persons, filename):
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump([person.to_dict() for person in persons], file, ensure_ascii=False, indent=4)

def save_to_xml(persons, filename):
    root = ET.Element('root')
    for i, item in enumerate(persons, 1):
        person = ET.SubElement(root, 'person' + str(i))
        ET.SubElement(person, 'ФИО').text = item.fio
        ET.SubElement(person, 'Страна').text = item.identity.country
        ET.SubElement(person, 'Паспортые_данные').text = item.identity.passport_data
        ET.SubElement(person, 'СНИЛС').text = item.identity.snils
        card = ET.SubElement(person, 'Карта')
        ET.SubElement(card, 'Номер_карты').text = item.card.card_number
        ET.SubElement(card, 'Банк').text = item.card.bank
        ET.SubElement(card, 'Платежная_система').text = item.card.payment_system
        for i, visit in enumerate(item.visits, 1):
            visit_root = ET.SubElement(person, "Визит" + str(i))
            ET.SubElement(visit_root, 'Симптомы').text = visit.symptoms
            ET.SubElement(visit_root, 'Врач').text = visit.doctor
            ET.SubElement(visit_root, 'Дата_посещения_врача').text = visit.date_of_visit
            ET.SubElement(visit_root, 'Анализы').text = visit.analysis
            ET.SubElement(visit_root, 'Дата_получения_анализов').text = visit.date_of_analysis
            ET.SubElement(visit_root, 'Цена_приёма').text = f'{visit.cost}руб.'
        tree = ET.ElementTree(root)
        tree.write(f'{filename}.xml', encoding='utf-8', xml_declaration=True)

def print_person(person):
    print(f"ФИО: {person.fio}")
    print(f"ID: {person.identity.id}")
    print(f"Паспорт: {person.identity.passport_data}")
    print(f"СНИЛС: {person.identity.snils}")
    print(f"Карта: {person.card.card_number}, {person.card.bank}, {person.card.payment_system}")

    for i, visit in enumerate(person.visits, 1):
        print(f"Визит {i}:")
        print(f"  Симптомы: {visit.symptoms}")
        print(f"  Врач: {visit.doctor}")
        print(f"  Дата визита: {visit.date_of_visit}")
        print(f"  Анализы: {visit.analysis}")
        print(f"  Дата получения анализов: {visit.date_of_analysis}")
        print(f"  Цена приёма: {visit.cost}")
    print("-" * 50)