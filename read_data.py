import json

f = open('persons.json')

data = json.load(f)

for i in data:
    print(i['Карта']['Платежная система'])
    # if i['Карта']['Платежная система'] == "Мир":
    #    print(i['ФИО'])
    # if i['Карта']['Платежная система'] == "MasterCard":
    #     print(i['ФИО'])
    # if i['Карта']['Платежя система'] == "Visa":
    #     print(i['ФИО'])

f.close()
