import re

from termcolor import colored
import requests
from bs4 import BeautifulSoup

place = 'CEDRITOS'
place = None
level = 'A1.2'
intensity = 'SEMI-INTENSIVO (SABADOS)'
places = ['CEDRITOS', 'CHICO', 'CENTRO']


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

  # if place and place not in content:
  #   continue

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
  print('Nivel:', colored(course.get('data-nivel'), 'red'))
  print('Intensidad:', colored(course.get('data-intensidad'), 'blue'))
  print('Cede:', colored(course_place, 'magenta'))
  print('Formato:', colored(course.get('data-formato'), 'yellow'))
  print('Estado:', 'Curso lleno' if 'Curso lleno' in content else 'disponible')

  for section in course.find_all('p'):
    strings = list(section.stripped_strings)
    if section.strong:
      title = process(section.strong.get_text())
      value = ' '.join(section.find_all(string=True, recursive=False))
      print(colored(title, 'green'), process(value))
