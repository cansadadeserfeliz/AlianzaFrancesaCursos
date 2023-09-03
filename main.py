import re

from termcolor import colored
import requests
from bs4 import BeautifulSoup

INTENCITY_SUPER_INTENCIVE = 'SUPER-INTENSIVO'
INTENCITY_INTENCIVE = 'INTENSIVO'
INTENCITY_WEEKDAYS = 'SEMI-INTENSIVO (SEMANA)'
INTENCITY_SATURDAY = 'SEMI-INTENSIVO (SABADOS)'

A1_LEVELS = ['A1.1', 'A1.2']
A2_LEVELS = ['A2.1', 'A2.2', 'A2.3']
A_LEVELS = A1_LEVELS + A2_LEVELS

B1_LEVELS = ['B1.1', 'B1.2', 'B1.3', 'B1.4', 'B1.5']
B2_LEVELS = ['B2.1', 'B2.2', 'B2.3', 'B2.4']
B_LEVELS = B1_LEVELS + B2_LEVELS

LEVELS = A_LEVELS + B_LEVELS

PLACE_CEDRITOS = 'CEDRITOS'
PLACES = [PLACE_CEDRITOS, 'CHICO', 'CENTRO']

COLOR_WHITE = 'white'
COLOR_GREEN = 'green'
COLOR_LIGHT_GREEN = 'light_green'
COLOR_RED = 'red'
COLOR_BLUE = 'blue'
COLOR_LIGHT_BLUE = 'light_blue'
COLOR_MAGENTA = 'magenta'
COLOR_LIGHT_YELLOW = 'light_yellow'

QUERY_PLACE = None
QUERY_LEVEL = A2_LEVELS[0]
QUERY_INTENSITY = INTENCITY_SATURDAY

input_message = 'Qué curso quieres consultar? \n'

enumerated_levels = {index + 1: level for index, level in enumerate(LEVELS)}
for index, item in enumerated_levels.items():
  input_message += f'{index}) {item}\n'
input_message += 'Escoge uno: '

QUERY_LEVEL = ''
while QUERY_LEVEL not in LEVELS:
  user_input = int(input(input_message))
  QUERY_LEVEL = enumerated_levels.get(user_input)

print('Escogiste: ' + QUERY_LEVEL)


def process(text):
  text = re.sub(' +', ' ', text)
  return text.strip().replace('\n', '')


print(colored('Cursos para adultos presenciales', COLOR_LIGHT_YELLOW), 'nivel',
      colored(QUERY_LEVEL, COLOR_RED), 'intensidad', QUERY_INTENSITY)

if QUERY_LEVEL.startswith('A1'):
  query_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/a1/'
elif QUERY_LEVEL.startswith('A2'):
  query_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/a2/'
elif QUERY_LEVEL.startswith('B1'):
  query_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/b1/'
elif QUERY_LEVEL.startswith('B2'):
  query_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/b2/'
elif QUERY_LEVEL.startswith('C1'):
  query_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/c1/'
elif QUERY_LEVEL.startswith('C2'):
  query_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/c2/'

response = requests.get(query_url)
assert response.status_code == 200

soup = BeautifulSoup(response.content, 'html.parser')
courses = soup.select('.cursos .curso')

for course in courses:
  content = course.text

  if QUERY_PLACE and QUERY_PLACE not in content:
    continue

  course_place = ''
  for p in PLACES:
    if p in content:
      course_place = p
      break

  if QUERY_LEVEL not in course.get('data-nivel'):
    continue

  if QUERY_INTENSITY not in course.get('data-intensidad'):
    continue

  print('--- === ---')
  print('Nivel:', colored(course.get('data-nivel'), COLOR_RED))
  print('Intensidad:', colored(course.get('data-intensidad'), COLOR_BLUE))
  print('Cede:', colored(course_place, COLOR_MAGENTA))
  print('Formato:', colored(course.get('data-formato'), COLOR_LIGHT_BLUE))
  print(
    'Estado:',
    colored('Curso lleno', COLOR_RED) if 'Curso lleno' in content else colored(
      'disponible', COLOR_GREEN))

  for section in course.find_all('p'):
    strings = list(section.stripped_strings)
    if section.strong:
      title = process(section.strong.get_text())

      value = ' '.join(section.find_all(string=True, recursive=False))
      value = process(value)

      color = COLOR_WHITE
      if title == 'Formato:':
        color = COLOR_LIGHT_GREEN

      print('\t', title, colored(value, color))

print('--- FIN ---')
