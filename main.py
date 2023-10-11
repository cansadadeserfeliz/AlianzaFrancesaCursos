import re
import os
import json

from termcolor import colored
import requests

# Page: https://afbogota.extranet-aec.com/classes/view/0-all/2-adultos/0-all-groups/0-all-levels/2-frances/#/

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
  return all([is_open, is_on_saturday])

output = list(filter(keep, response_json))

for item in output:
  print('Curso:', item['class_name'])
  print('Sede:', item['etablishmentBranchName'])
  print('Inicio:', item['date_start'])
  print('Fin:', item['date_end'])
  for schedule in item['schedules']:
    print('Días:', schedule['dates'])
    print('Hora:', schedule['start_time'])
  print('-' * 20, '\n')
