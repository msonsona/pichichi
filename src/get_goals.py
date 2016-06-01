#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import csv

page = requests.get('http://www.marca.com/futbol/primera/calendario.html')
soup = BeautifulSoup(page.content, 'html.parser')

goles = []
goleadores = {}
id_gol = 1

with open('goles.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Gol', 'Jornada', 'Minuto', 'Equipo', 'Goleador', 'Rival', 'Local', 'Resultado', 'Resultado Final', 'Penalty', 'Propia Puerta'])
    
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
            
                pag_partido = requests.get(partido_url)
                partido_soup = BeautifulSoup(pag_partido.content, 'html.parser')
            
                marcador = partido_soup.find('div', class_='marcador')
            
                marcador_local = marcador.find('div', class_='equipo-1')
                marcador_visitante = marcador.find('div', class_='equipo-2')
            
                num_goles_local = marcador_local.find('div', class_='resultado').text
                num_goles_visitante = marcador_visitante.find('div', class_='resultado').text
                resultado_final = '{}-{}'.format(num_goles_local,num_goles_visitante)
            
                goleadores_local = marcador_local.find('div', class_='goles')
                goleadores_visitante = marcador_visitante.find('div', class_='goles')
            
                goles_local = goleadores_local.ul.find_all('li')
                goles_visitante = goleadores_visitante.ul.find_all('li')
                
                for gol in goles_local:
                    resultado = gol.span.text
                    gol.span.clear()
                    goleador = gol.text.split('(')[0].strip()
                    token = gol.text.split('(')[1].lower()
                    if token.count('p') > 0:
                        minuto = gol.text.split('(')[2].strip("')")
                        if token.count('p') == 1:
                            penalty = 1
                        else:
                            propia_puerta = 1
                    else:
                        minuto = gol.text.split('(')[1].strip("')")
                        penalty = 0
                        propia_puerta = 0
                    
                    if goleador not in goleadores:
                        goleadores[goleador] = 0
                    goleadores[goleador] += 1
                    
                    csv_writer.writerow([id_gol, num_jornada, minuto, local, goleador, visitante, 1, resultado, resultado_final, penalty, propia_puerta])
                    id_gol += 1
                
                for gol in goles_visitante:
                    resultado = gol.span.text
                    gol.span.clear()
                    goleador = gol.text.split('(')[0].strip()
                    token = gol.text.split('(')[1].lower()
                    if token.count('p') > 0:
                        minuto = gol.text.split('(')[2].strip("')")
                        if token.count('p') == 1:
                            penalty = 1
                        else:
                            propia_puerta = 1
                    else:
                        minuto = gol.text.split('(')[1].strip("')")
                        penalty = 0
                        propia_puerta = 0
                    
                    if goleador not in goleadores:
                        goleadores[goleador] = 0
                    goleadores[goleador] += 1
                    
                    csv_writer.writerow([id_gol, num_jornada, minuto, visitante, goleador, local, 0, resultado
                    , resultado_final, penalty, propia_puerta])
                    id_gol += 1
            
            else:
                print("No url")
            
    print(goleadores)