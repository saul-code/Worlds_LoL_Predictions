# Worlds_LoL_Predictions
Prediccion de ganador en una serie mejor de 5 entre dos equipos de League of Legends que hayan jugando mundiales de League of Legends

## Prediccion de Ganador en un mejor de 5

### Paso 1: Calcula la media de victorias (λ)
Primero, necesitamos calcular la tasa promedio (λ, lambda) de victorias de tu equipo de interés (digamos, el Equipo A) cuando juega series al mejor de cinco. Esto se basa en datos históricos. Calcularemos el promedio de victorias como la suma de puntos de cada equipo ente el número de las series jugadas.


### Paso 2: Aplicar la fórmula de Poisson
La fórmula de la distribución de Poisson es:
```math
P(k; λ) = \frac{λ^k e^{-λ}}{k!}
```
Donde:
- $P(k; λ)$ es la probabilidad de que ocurran \(k\) eventos (en este caso, victorias) cuando el promedio es \(λ\).
- \(k\) es el número de eventos que nos interesa calcular la probabilidad (por ejemplo, necesitamos al menos 3 victorias para ganar una serie al mejor de cinco).
- \(λ\) es el promedio de eventos (victorias) que calculamos en el paso 1.
- \(e\) es la base de los logaritmos naturales.

### Paso 3: Calcular la probabilidad de ganar la serie
Para ganar una serie al mejor de cinco, el Equipo A necesita ganar  3 partidos. Calcularemos la probabilidad de cada uno de los escenarios como 3-2 , 3-1, 3-0.


## Ejecucion del programa
1. ```pip install -r requirements.txt``` para tener las librerias necesarias
2. Debemos estar en el src/ y ejecutamos ```python3 Main.py```
