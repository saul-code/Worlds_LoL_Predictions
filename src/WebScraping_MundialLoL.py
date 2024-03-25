#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import pandas as pd

years = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

def get_matches(year):
   """
     Obtiene todos los partidos y los puntos del mundial de League of Legends de cada año en la fase de grupos
  
    Args:
         year(int): año que quieres obtener datos
            
    Returns:      
          df_matches (pd.DataFrame): DataFrame con datos de partidos de ese año.
      """

  if (year >= 2014):
    web = f'https://lol.fandom.com/wiki/{year}_Season_World_Championship'
  else:
    web = f'https://lol.fandom.com/wiki/Season_{str(year)[3]}_World_Championship'

  response = requests.get(web)
  soup = BeautifulSoup(response.content,'html.parser')
  matches = soup.find_all('div', class_ ='crossbox-outer')

  if ((year > 2013 and year<2017) or year == 2012):
    # Quitamos la tabla de partidos entre regiones
    matches.pop()

  resultados_matches = []
  teamA =[]
  teamB = []
  score = []

  for match in matches:
    tabla_matches = match.find('table')

    for row in tabla_matches.find_all('tr')[1:]:
      team1 = row.find('th')['title']

      for cell in row.find_all('td'):
        if 'crossbox-mirror' in cell.get('class', []):
              continue
        if 'data-crossbox-highlight-vs' in cell.attrs:
          team2 = cell['data-crossbox-highlight-vs']  # Nombre del segundo equipo (team2)
          result = cell.get_text(strip=True)  # Resultado del enfrentamiento
          if team1 != team2:  # Asegurarse de que no es el equipo contra sí mismo
            teamA.append(team1)
            score.append(result)
            teamB.append(team2)

  dict_matches_resultado = {'Team A': teamA, 'score':score,'Team B':teamB,'year':year}
  df_matches = pd.DataFrame(dict_matches_resultado)
  return df_matches

#Generamos el archivo csv para todos los años en la lista years
mundial_Lol = [get_matches(year) for year in years]
df_mundial_Lol=pd.concat(mundial_Lol, ignore_index = True)
df_mundial_Lol.to_csv('data_historica_de_LoL.csv',index=False)





