import matplotlib.pyplot as plt
import pandas as pd
from math import exp, factorial
import sys
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
          tuple: (prob_A, prob_B,ganador) donde prob_A es la probabilidad de que el equipo A gane y prob_B es la probabilidad de que el equipo B gane.
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
    if(prob_A_wins_series > prob_B_wins_series):
      return prob_A_wins_series, prob_B_wins_series,teamA
    else:
      return prob_A_wins_series, prob_B_wins_series,teamB

def main():
  df_data_historica = pd.read_csv('data_historica_de_LoL.csv')    
  team_A = str(input("Equipo 1: "))
  team_B = str(input("Equipo 2: "))

  busqueda1 =(df_data_historica.loc[df_data_historica['Team A'] == team_A])
  busqueda2 = (df_data_historica.loc[df_data_historica['Team B'] == team_B])
  if (busqueda1.empty) or (busqueda2.empty):
    print(f'No se encontro los equipos: {team_A} o {team_B}')
  else:    
    prob_A, prob_B,ganador = poisson_probability(team_A,team_B, df_data_historica)
    print(f'{team_A} vs {team_B} en una serie de mejor de 5 ganaria {ganador}\n')
    print(f'{team_A} con probabilidad de {prob_A}')
    print(f'{team_B} con probabilidad de {prob_B}')


if __name__ == "__main__":
    main()