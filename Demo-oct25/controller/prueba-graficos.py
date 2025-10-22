from chart_creator import chart
import sys
import os

# Agrega la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.gral import General


gral = General()

csv_name= "entradas_salidas.csv"
csv_out_svg= "graf_base1_csv.svg"
csv_file = gral.get_file_base_csv(f"{csv_name}")
grafica1= chart.graf_base1_csv(csv_file, csv_out_svg)
print("Gráfica generada en:", grafica1)