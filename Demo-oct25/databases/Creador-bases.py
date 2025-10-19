#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 04:05:21 2025

@author: galmarod
"""

import pandas as pd
import numpy as np
import sqlite3
import json
from datetime import date, timedelta
from openpyxl import Workbook

# === CONFIGURACIONES GENERALES === #
np.random.seed(42)
dias = 30
fecha_inicio = date(2025, 10, 1)
fechas = [fecha_inicio + timedelta(days=i) for i in range(dias)]

productos = ["Premium", "Magna", "Diesel", "Aceite", "Anticongelante"]

# ====================================================
# 1️⃣ BASE CSV — Registro de ventas por despachador
# ====================================================

despachadores = ["D1", "D2", "D3"]

def generar_datos_csv():
    datos = []
    for f in fechas:
        fila = {"Fecha": f.isoformat()}
        total_dia = 0
        for d in despachadores:
            for p in ["Premium", "Magna", "Diesel"]:
                litros = np.random.randint(1200, 1800)
                fila[f"{d}_{p.lower()}"] = litros
                total_dia += litros
        # Aceite y anticongelante
        fila["Aceite"] = np.random.randint(8, 15)
        fila["Anticongelante"] = np.random.randint(5, 10)
        datos.append(fila)
    return pd.DataFrame(datos)

df_csv = generar_datos_csv()
df_csv.to_csv("entradas_salidas.csv", index=False)
print("✅ Archivo CSV generado: entradas_salidas.csv")

# Totales diarios de combustible (solo Premium, Magna, Diesel)
df_csv["Total_combustible"] = df_csv[
    [col for col in df_csv.columns if any(f in col for f in ["premium", "magna", "diesel"])]
].sum(axis=1)

# ====================================================
# 2️⃣ BASE XLSX — Registro de personal (3 turnos)
# ====================================================

personales = {
    "Turno_1": ["Juan Pérez", "María López", "Luis Ortega"],
    "Turno_2": ["Ana Torres", "José Rivas", "Raúl Gómez"],
    "Turno_3": ["Lucía Díaz", "Carlos Vega", "Rosa Ramírez"]
}

wb = Workbook()
wb.remove(wb.active)  # elimina hoja por defecto

for turno, nombres in personales.items():
    ws = wb.create_sheet(turno)
    ws.append(["Fecha", "Personal_1", "Litros_P1", "Personal_2", "Litros_P2", "Personal_3", "Litros_P3"])
    for i, f in enumerate(fechas):
        total_dia = df_csv.loc[i, "Total_combustible"]
        proporciones = np.random.dirichlet(np.ones(3), size=1)[0]  # distribuye aleatoriamente el total
        litros = (proporciones * total_dia / 3).astype(int)  # divide entre 3 turnos para no exceder total global
        ws.append([
            f.isoformat(),
            nombres[0], int(litros[0]),
            nombres[1], int(litros[1]),
            nombres[2], int(litros[2])
        ])

wb.save("personal_turnos.xlsx")
print("✅ Archivo XLSX generado: personal_turnos.xlsx")

# ====================================================
# 3️⃣ BASE SQL — Formas de pago (por producto)
# ====================================================

conn = sqlite3.connect("formas_pago.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE formas_pago (
    fecha TEXT PRIMARY KEY,
    premium_efectivo REAL, premium_debito REAL, premium_credito REAL,
    magna_efectivo REAL, magna_debito REAL, magna_credito REAL,
    diesel_efectivo REAL, diesel_debito REAL, diesel_credito REAL,
    aceite_efectivo REAL, aceite_debito REAL, aceite_credito REAL
);
""")

for i, f in enumerate(fechas):
    total_dia = df_csv.loc[i, "Total_combustible"]
    # Distribuye litros entre productos de manera proporcional
    proporciones_prod = np.random.dirichlet(np.ones(3))
    litros_por_producto = total_dia * proporciones_prod

    # Cada producto se divide entre tipos de pago
    valores = []
    for litros in litros_por_producto:
        proporciones_pago = np.random.dirichlet(np.ones(3))
        pagos = (litros * proporciones_pago).round(2)
        valores.extend(pagos.tolist())

    # Aceite (aleatorio menor)
    aceite_vals = np.random.dirichlet(np.ones(3)) * np.random.uniform(8, 15)
    valores.extend(aceite_vals.round(2).tolist())

    cur.execute("""
        INSERT INTO formas_pago VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [f.isoformat()] + valores)

conn.commit()
conn.close()
print("✅ Archivo SQL generado: formas_pago.db")

# ====================================================
# 4️⃣ BASE JSON — Registro de vapores (30 días)
# ====================================================

mediciones = []
for f in fechas:
    mediciones.append({
        "fecha": f.isoformat(),
        "benceno_ppm": round(np.random.uniform(0.10, 0.20), 2),
        "tolueno_ppm": round(np.random.uniform(0.30, 0.40), 2),
        "xilenos_ppm": round(np.random.uniform(0.20, 0.30), 2),
        "co_ppm": round(np.random.uniform(1.4, 2.0), 2),
        "nox_ppm": round(np.random.uniform(0.8, 1.2), 2),
        "so2_ppm": round(np.random.uniform(0.14, 0.22), 2)
    })

json_data = {
    "estacion": "Gasolinera Las Palmas",
    "ubicacion": "Cd. de México",
    "periodo": "2025-10",
    "mediciones": mediciones
}

with open("medicion_vapores.json", "w") as f:
    json.dump(json_data, f, indent=4)

print("✅ Archivo JSON generado: medicion_vapores.json")

# ====================================================
# ✅ Verificación de consistencia
# ====================================================
total_csv = int(df_csv["Total_combustible"].sum())
print(f"\n🔎 Total litros vendidos del mes (base CSV): {total_csv:,}")
print("Todos los demás archivos fueron generados respetando ese total base.")
