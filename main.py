import re
import os
import json

from termcolor import colored
import requests

# Page: https://afbogota.extranet-aec.com/classes/view/0-all/2-adultos/0-all-groups/0-all-levels/2-frances/#/

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
  is_on_saturday = any([item['days_representation'] == 'Sábado' for item in data['schedules']])
  is_not_center = data['etablishmentBranchName'] != 'Sede Centro'
  return all([is_open, is_on_saturday, is_not_center])

output = list(filter(keep, response_json))

for item in output:
  print('Curso:', colored(item['class_name'], COLOR_RED))
  print('Sede:', item['etablishmentBranchName'])
  print('Inicio:', item['date_start'])
  print('Fin:', item['date_end'])
  for schedule in item['schedules']:
    print('Días:', schedule['dates'])
    print('Hora:', schedule['start_time'])
  print('-' * 20, '\n')
