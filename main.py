import re

from termcolor import colored
import requests
from bs4 import BeautifulSoup

place = 'CEDRITOS'
place = None
level = 'A2.1'
intensity = 'SEMI-INTENSIVO (SABADOS)'
places = ['CEDRITOS', 'CHICO', 'CENTRO']

COLOR_WHITE = 'white'
COLOR_GREEN = 'green'
COLOR_LIGHT_GREEN = 'light_green'
COLOR_RED = 'red'
COLOR_BLUE = 'blue'
COLOR_LIGHT_BLUE = 'light_blue'
COLOR_MAGENTA = 'magenta'
COLOR_LIGHT_YELLOW = 'light_yellow'


def process(text):
  text = re.sub(' +', ' ', text)
  return text.strip().replace('\n', '')


if level.startswith('A1'):
  course_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/a1/'
elif level.startswith('A2'):
  course_url = 'https://alianzafrancesa.edu.co/bogota/cursos-y-examenes/a2/'

response = requests.get(course_url)
assert response.status_code == 200

soup = BeautifulSoup(response.content, 'html.parser')
courses = soup.select('.cursos .curso')

for course in courses:
  content = course.text

  if place and place not in content:
    continue

  course_place = ''
  for p in places:
    if p in content:
      course_place = p
      break

  if level not in course.get('data-nivel'):
    continue

  if intensity not in course.get('data-intensidad'):
    continue

  print('--- === ---')
  print('Nivel:', colored(course.get('data-nivel'), COLOR_RED))
  print('Intensidad:', colored(course.get('data-intensidad'), COLOR_BLUE))
  print('Cede:', colored(course_place, COLOR_MAGENTA))
  print('Formato:', colored(course.get('data-formato'), COLOR_LIGHT_BLUE))
  print('Estado:', colored('Curso lleno', COLOR_RED) if 'Curso lleno' in content else colored('disponible', COLOR_GREEN))

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
