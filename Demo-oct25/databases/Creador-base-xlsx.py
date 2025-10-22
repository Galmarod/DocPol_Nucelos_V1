from openpyxl import Workbook
import pandas as pd
import numpy as np

# Personal por turno
personales = {
    "Turno_1": ["Juan Pérez", "María López", "Luis Ortega"],
    "Turno_2": ["Ana Torres", "José Rivas", "Raúl Gómez"],
    "Turno_3": ["Lucía Díaz", "Carlos Vega", "Rosa Ramírez"]
}

# Fechas simuladas (1 mes)
fechas = pd.date_range("2025-10-01", "2025-10-30", freq="D")

# Simulación de totales de combustible (de otra base CSV)
np.random.seed(42)
total_combustible = np.random.randint(3000, 6000, size=len(fechas))

wb = Workbook()
wb.remove(wb.active)

# --- Rotar personal entre turnos ---
todos_personales = sum(personales.values(), [])  # lista plana con todos los nombres

for turno in personales.keys():
    ws = wb.create_sheet(turno)
    ws.append(["Fecha", "Personal_1", "Litros_P1", "Personal_2", "Litros_P2", "Personal_3", "Litros_P3"])

    for i, f in enumerate(fechas):
        total_dia = total_combustible[i]
        proporciones = np.random.dirichlet(np.ones(3), size=1)[0]
        litros = (proporciones * total_dia / 3).astype(int)
        
        # Rotación: cada día cambia el grupo de personas
        rotados = np.roll(todos_personales, i)[:3]  # 3 por turno

        ws.append([
            f.date().isoformat(),
            rotados[0], int(litros[0]),
            rotados[1], int(litros[1]),
            rotados[2], int(litros[2])
        ])

wb.save("personal_turnos.xlsx")
print("✅ Archivo XLSX generado con rotación de turnos: personal_turnos.xlsx")
