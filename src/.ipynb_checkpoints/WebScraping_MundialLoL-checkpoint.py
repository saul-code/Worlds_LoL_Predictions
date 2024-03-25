#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/saul-code/Worlds_LoL_Predictions/blob/main/AnalizadorDatosLoL.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[ ]:


from bs4 import BeautifulSoup
import requests
import pandas as pd

years = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

def get_matches(year):

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

mundial_Lol = [get_matches(year) for year in years]
df_mundial_Lol=pd.concat(mundial_Lol, ignore_index = True)
df_mundial_Lol.to_csv('data_historica_de_LoL.csv',index=False)


# ## Prediccion de Ganador en un mejor de 5
# 
# ### Paso 1: Calcula la media de victorias (λ)
# Primero, necesitamos calcular la tasa promedio (λ, lambda) de victorias de tu equipo de interés (digamos, el Equipo A) cuando juega series al mejor de cinco. Esto se basa en datos históricos. Calcularemos el promedio de victorias como la suma de puntos de cada equipo ente el número de las series jugadas.
# 
# 
# ### Paso 2: Aplicar la fórmula de Poisson
# La fórmula de la distribución de Poisson es:
# $ P(k; λ) = \frac{λ^k e^{-λ}}{k!}$
# Donde:
# - $P(k; λ)$ es la probabilidad de que ocurran \(k\) eventos (en este caso, victorias) cuando el promedio es \(λ\).
# - \(k\) es el número de eventos que nos interesa calcular la probabilidad (por ejemplo, necesitamos al menos 3 victorias para ganar una serie al mejor de cinco).
# - \(λ\) es el promedio de eventos (victorias) que calculamos en el paso 1.
# - \(e\) es la base de los logaritmos naturales.
# 
# ### Paso 3: Calcular la probabilidad de ganar la serie
# Para ganar una serie al mejor de cinco, el Equipo A necesita ganar  3 partidos. Calcularemos la probabilidad de cada uno de los escenarios como 3-2 , 3-1, 3-0.
# 
# 

# In[77]:


import matplotlib.pyplot as plt
from math import exp, factorial

# Función de Poisson
def poisson(k, lambda_):
    return (lambda_ ** k) * exp(-lambda_) / factorial(k)


def poisson_probability(teamA, teamB, df_data_historica):
    """
    Calcula la probabilidad de que el equipo A gane al equipo B en un formato de mejor de 5 utilizando la distribución de Poisson.

    Args:
        teamA (str): Nombre del equipo A.
        teamB (str): Nombre del equipo B.
        df_data_historica (pd.DataFrame): DataFrame con datos históricos de partidos.

    Returns:
        tuple: (prob_A, prob_B) donde prob_A es la probabilidad de que el equipo A gane y prob_B es la probabilidad de que el equipo B gane.
    """
    # Calcula los puntos promedio marcados por cada equipo
    points_for_A = df_data_historica[df_data_historica['Team A'] == teamA]['score'].str.split('-').apply(lambda x: int(x[0])).mean()
    points_for_B = df_data_historica[df_data_historica['Team B'] == teamB]['score'].str.split('-').apply(lambda x: int(x[1])).mean()

    # Inicializa las probabilidades de que cada equipo gane la serie
    prob_A_wins_series = 0
    prob_B_wins_series = 0

    # Calcula la probabilidad de que cada equipo gane 0 a 3 partidos utilizando la distribución de Poisson
    probs_A = [poisson(k, points_for_A) for k in range(4)]
    probs_B = [poisson(k, points_for_B) for k in range(4)]


    # Calcula las combinaciones donde un equipo gana la serie
    for i in range(1, 4):  # Un equipo necesita ganar al menos 3 partidas para ganar la serie
        for j in range(0, i):
            prob_A_wins_series += probs_A[i] * probs_B[j]  # Probabilidad de que A gane i partidas y B gane j partidas
            prob_B_wins_series += probs_A[j] * probs_B[i]  # Inverso para B
    if(prob_A > prob_B):
      return prob_A_wins_series, prob_B_wins_series,teamA
    else:
      return prob_A_wins_series, prob_B_wins_series,teamB

# Ejemplo de uso con equipos ficticios y datos históricos (df_data_historica debería estar definido previamente)
team_A = 'T1'
team_B = 'EDward Gaming'
prob_A, prob_B,ganador = poisson_probability(team_A,team_B, df_data_historica)
print(f'{team_A} vs {team_B} en una serie de mejor de 5 ganaria {ganador}\n')
print(f'{team_A} con probabilidad de {prob_A}')
print(f'{team_B} con probabilidad de {prob_B}')


# In[ ]:




