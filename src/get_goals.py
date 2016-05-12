#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.marca.com/futbol/primera/calendario.html')
soup = BeautifulSoup(page.content, 'html.parser')

for jornada in soup.find_all('div', class_='jornadaCalendario'):
    num_jornada = jornada.div.h2.text.split()[1]
    print(jornada.div.h2.text)
    partidos = jornada.ul.find_all('li')
    
    for partido in partidos:
        print(partido.h3.a['title'])
        local = partido.h3.a.find('span', class_='local').text
        visitante = partido.h3.a.find('span', class_='visitante').text
        resultado = partido.h3.a.find('span', class_='resultado').text
        
        if partido.h3.a.has_attr('href'):
            partido_url = partido.h3.a['href']
            print(partido_url)
        else:
            print("No url")