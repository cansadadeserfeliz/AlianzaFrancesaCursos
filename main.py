import os
import locale
import json

from termcolor import colored
import requests

# Page: https://afbogota.extranet-aec.com/classes/view/0-all/2-adultos/0-all-groups/0-all-levels/2-frances/#/

locale.setlocale(locale.LC_ALL, '')

COLOR_WHITE = 'white'
COLOR_GREEN = 'green'
COLOR_LIGHT_GREEN = 'light_green'
COLOR_RED = 'red'
COLOR_BLUE = 'blue'
COLOR_LIGHT_BLUE = 'light_blue'
COLOR_MAGENTA = 'magenta'
COLOR_LIGHT_YELLOW = 'light_yellow'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://afbogota.extranet-aec.com/',
    'Extranet_session': os.environ['AF_SESSION_KEY'],
    'Api_key': os.environ['AF_API_KEY'],
}
response = requests.get(
    'https://afbogota.aec-app.com/arc-en-ciel/api/public/core/v1/courses',
    headers=headers)
response_json = response.json()


def keep(data):
    is_open = data['status'] == 'OPEN'
    is_on_saturday = any([
        item['days_representation'] == 'Sábado' for item in data['schedules']
    ])
    is_not_center = data['etablishmentBranchName'] != 'Sede Centro'
    location = data['classLocation']
    is_not_online = location != 'ONLINE' and location != 'EXTRAMUROS'
    return all([is_open, is_on_saturday, is_not_center, is_not_online])


output = list(filter(keep, response_json))

# Output sample: https://gist.github.com/cansadadeserfeliz/29426ad16a60a45a8373fe76a0138c7d

LEVEL_TO_HIGHLIGHT = 'A2'
for item in output:
    print(
        'Curso:',
        colored(
            item['levelTitle'], COLOR_LIGHT_YELLOW
            if LEVEL_TO_HIGHLIGHT in item['levelTitle'] else COLOR_BLUE),
        '>',
        item['class_name'],
        item['classLocation'],
    )
    print('Sede:', colored(item['etablishmentBranchName'], COLOR_GREEN))
    print('Inscripciones desde', item['date_start_enroll'], 'hasta',
          item['date_end_enroll'])
    print('Fechas:', colored(item['date_start'], COLOR_LIGHT_GREEN), '>',
          item['date_end'])
    print('Presio:', locale.currency(item['class_price'], grouping=True))

    for schedule in item['schedules']:
        print('Días:', schedule['dates'],
              f'({colored(schedule["days_representation"], COLOR_MAGENTA)})')
        print(
            'Hora:',
            schedule['start_time'],
            '>',
            schedule['end_time'],
            f"({schedule['classroom']})",
        )

    print(f"Estudiantes {item['qty_student']}/{item['max_student']}"
          f" (dispinibles: {item['qty_available_seats']})")
    print('Libros', ', '.join(item['books']))
    print('-' * 20, '\n')
