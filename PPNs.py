#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re
import glob
from collections import defaultdict

# Cargar datos de la tabla de rasgos
df = pd.read_csv('ROSMAP-Trait_ordenado.txt', delimiter='\t')

# Inicializar listas para almacenar specimenID según el diagnóstico
lista_cogdx_NCI = []  # NCI=1.0
lista_cogdx_AD = []   # AD=4.0

# Clasificar specimenID según el diagnóstico
for index, row in df.iterrows():
    specimenID = row['specimenID']
    cogdx = row['cogdx']
    if cogdx == 1.0:
        lista_cogdx_NCI.append((specimenID, cogdx))
    else:
        lista_cogdx_AD.append((specimenID, cogdx))

# Directorio donde se encuentran los archivos CSV
directorio_archivos = '/'

# Función para cargar archivos y concatenar datos
def cargar_y_concatenar(lista_specimenID, sufijo):
    df_concatenado = pd.DataFrame()
    for specimenID, _ in lista_specimenID:
        archivos_coincidentes = glob.glob(f'{directorio_archivos}red_pp_{specimenID}_*_expscore_01-dbscore01.csv')
        for archivo in archivos_coincidentes:
            df_archivo = pd.read_csv(archivo, usecols=[0, 1], delimiter='\t')
            df_concatenado[specimenID] = df_archivo.apply(lambda row: f'{row.iloc[0]}, {row.iloc[1]}', axis=1)
    df_concatenado.to_csv(f'valores_concatenados_{sufijo}.csv', index=False)

# Cargar y concatenar datos para NCI y AD
cargar_y_concatenar(lista_cogdx_NCI, 'NCI')
cargar_y_concatenar(lista_cogdx_AD, 'AD')

# Cargar DataFrames de los archivos concatenados
df_AD = pd.read_csv('subset_valores_concatenados_AD.csv')
df_NCI = pd.read_csv('subset_valores_concatenados_NCI.csv')

# Obtener todas las asociaciones proteína-proteína
asociaciones_AD = list(set(df_AD.stack().explode().unique()))
asociaciones_NCI = list(set(df_NCI.stack().explode().unique()))
asociaciones = list(set(asociaciones_AD) | set(asociaciones_NCI))

# Crear DataFrame para resultados
df_resultado_AD = pd.DataFrame(0, index=asociaciones_AD, columns=df_AD.columns)
df_resultado_NCI = pd.DataFrame(0, index=asociaciones_NCI, columns=df_NCI.columns)

# Llenar DataFrames con 1 si la asociación está presente
for muestra in df_AD.columns:
    for asociacion in asociaciones_AD:
        df_resultado_AD.at[asociacion, muestra] = 1 if (df_AD[muestra].explode() == asociacion).any() else 0

for muestra in df_NCI.columns:
    for asociacion in asociaciones_NCI:
        df_resultado_NCI.at[asociacion, muestra] = 1 if (df_NCI[muestra].explode() == asociacion).any() else 0

# Función para realizar bootstrap y calcular frecuencias
def bootstrap_frecuencias(df_resultado, n_bootstrap=1000, n_muestras=50):
    frecuencias = defaultdict(int)
    for _ in range(n_bootstrap):
        muestras_bootstrap = np.random.choice(df_resultado.columns, size=n_muestras, replace=True)
        for asociacion in df_resultado.index:
            if any(df_resultado.loc[asociacion, muestras_bootstrap] == 1):
                frecuencias[asociacion] += 1
    return frecuencias

# Calcular frecuencias para AD y NCI
frecuencias_AD = bootstrap_frecuencias(df_resultado_AD)
frecuencias_NCI = bootstrap_frecuencias(df_resultado_NCI)

# Identificar asociaciones frecuentes (80% de las veces)
umbral = 0.8 * 10  # 80% de 10 iteraciones
asociaciones_frecuentes_AD = {k: v for k, v in frecuencias_AD.items() if v >= umbral}
asociaciones_frecuentes_NCI = {k: v for k, v in frecuencias_NCI.items() if v >= umbral}

# Mostrar resultados
print("Asociaciones frecuentes en individuos AD:")
for asociacion, frecuencia in asociaciones_frecuentes_AD.items():
    print(f"Asociación: {asociacion}, Frecuencia: {frecuencia}")

print("\nAsociaciones frecuentes en individuos NCI:")
for asociacion, frecuencia in asociaciones_frecuentes_NCI.items():
    print(f"Asociación: {asociacion}, Frecuencia: {frecuencia}")