#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from collections import defaultdict
from scipy.stats import chi2_contingency
import statsmodels.stats.multitest as smm

# Cargar datos
df_AD = pd.read_csv('/valores_concatenados_apoe_carriers.csv')

# Obtener asociaciones proteína-proteína
muestras_AD = df_AD.columns.tolist()
asociaciones_AD = list(set(df_AD.stack().explode().unique()))
df_resultado_AD = pd.DataFrame(columns=muestras_AD, index=asociaciones_AD)

# Llenar el DataFrame con 1 si la asociación está presente o 0 si está ausente
for muestra_AD in muestras_AD:
    for asociacion_AD in asociaciones_AD:
        df_resultado_AD.at[asociacion_AD, muestra_AD] = 1 if (muestra_AD in df_AD.columns and (df_AD[muestra_AD].explode() == asociacion_AD).any()) else 0

# Rellenar celdas vacías con 0
df_resultado_AD = df_resultado_AD.fillna(0)

# Bootstrap para la población
n_bootstrap = 1000
n_muestras_bootstrap = 50
frecuencias_bootstrap_poblacion = defaultdict(int)
df_frecuencias_bootstrap = pd.DataFrame(index=asociaciones_AD)

for i in range(n_bootstrap):
    pacientes_poblacion_bootstrap = np.random.choice(df_resultado_AD.columns, size=n_muestras_bootstrap, replace=True)
    frecuencias_asociaciones_bootstrap = df_resultado_AD[pacientes_poblacion_bootstrap].sum(axis=1)
    df_frecuencias_bootstrap[f"Iteración_{i+1}"] = frecuencias_asociaciones_bootstrap
    for asociacion, frecuencia in frecuencias_asociaciones_bootstrap.items():
        frecuencias_bootstrap_poblacion[asociacion] += frecuencia

# Identificar asociaciones frecuentes
umbral_global = 0.8 * n_bootstrap
asociaciones_frecuentes_poblacion = {asociacion: frecuencia for asociacion, frecuencia in frecuencias_bootstrap_poblacion.items() if frecuencia >= umbral_global}

# Guardar resultados
df_frecuencias_bootstrap.to_csv('/media/vero/RESPALDO_PC/Paper_3/Prueba-GRNscript/GRNs/df_frecuencias_iteraciones-bootstrap_carriers.csv')

# Análisis de Chi-cuadrado
# (Se asume que se han cargado datos de frecuencias para AD y sanos en DataFrames separados)
# Aquí se debe implementar el análisis de Chi-cuadrado como se describió en el código original.
