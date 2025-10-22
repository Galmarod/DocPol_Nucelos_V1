#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Guillermo Almanza Rodríguez"
__copyright__  = "Copyright 2025, RevelCode"
__credits__    = ["galmarod"]
__license__    = "GPL"
__version__    = "1.0.0"
__maintainer__ = "Guillermo Almanza Rodríguez"
__email__      = "galmarod@gmail.com"
__status__     = "Development"
__date__       = "Oct-2025"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # carpeta raíz del proyecto
ASSETS_DIR = os.path.join(BASE_DIR, "assests")
# Crear la carpeta si no existe
os.makedirs(ASSETS_DIR, exist_ok=True)

class chart:

    # ==============================================================
    # ====== Graficación de entradas y salidas de combustible ======
    # ==============================================================
    def graf_base1_csv(CSV_FILE,OUT_SVG):
        df = pd.read_csv(CSV_FILE, parse_dates=["Fecha"])

        # Sumar por producto
        premium_cols = [c for c in df.columns if "premium" in c.lower()]
        magna_cols = [c for c in df.columns if "magna" in c.lower()]
        diesel_cols = [c for c in df.columns if "diesel" in c.lower()]

        df["Total_Litros"] = df[premium_cols + magna_cols + diesel_cols].sum(axis=1)

        plt.figure(figsize=(12, 6))
        plt.scatter(df["Fecha"], df["Total_Litros"], color="royalblue", label="Total diario", alpha=0.8)
        plt.plot(df["Fecha"], df["Total_Litros"], color="lightblue", linewidth=1)

        plt.title("Dispersión de litros vendidos por día", fontsize=13)
        plt.xlabel("Fecha")
        plt.ylabel("Litros vendidos")
        plt.xticks(rotation=90)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.legend()

        # Construir ruta completa en assets
        out_svg_path = os.path.join(ASSETS_DIR, OUT_SVG)

        plt.savefig(out_svg_path, format="svg")
        print(f"SVG guardado en: {os.path.abspath(out_svg_path)}")
        plt.close()
        
        return out_svg_path
    
    def graf_base2_xlsx(XLSX_FILE,OUT_SVG):
        xls = pd.ExcelFile(XLSX_FILE)
        turno_totales = {}

        for turno in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=turno)
            turno_id = turno.split("_")[-1]
            for i in range(1, 4):
                pcol = f"Personal_{i}"
                lcol = f"Litros_P{i}"
                if pcol in df.columns and lcol in df.columns:
                    grouped = df.groupby(pcol)[lcol].sum()
                    for name, litros in grouped.items():
                        if name not in turno_totales:
                            turno_totales[name] = {"1": 0, "2": 0, "3": 0}
                        turno_totales[name][turno_id] += litros

        # Crear DataFrame
        plot_df = pd.DataFrame(turno_totales).T.fillna(0)
        plot_df = plot_df[["1", "2", "3"]]
        plot_df.columns = ["Turno 1", "Turno 2", "Turno 3"]

        # --- Graficar barras agrupadas ---
        x = np.arange(len(plot_df))
        width = 0.25

        fig, ax = plt.subplots(figsize=(13, 6))
        bars1 = ax.bar(x - width, plot_df["Turno 1"], width, label="Turno 1")
        bars2 = ax.bar(x, plot_df["Turno 2"], width, label="Turno 2")
        bars3 = ax.bar(x + width, plot_df["Turno 3"], width, label="Turno 3")

        # Etiquetas de valores
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                        f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=8)

        # Ejes
        ax.set_xticks(x)
        ax.set_xticklabels(plot_df.index, rotation=45, ha='right')
        ax.set_ylabel("Litros vendidos (mes)")
        ax.set_title("Litros vendidos por persona y turno (rotación mensual)")
        ax.legend()
        ax.grid(True, axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()

        # Construir ruta completa en assets
        out_svg_path = os.path.join(ASSETS_DIR, OUT_SVG)

        plt.savefig(out_svg_path, format="svg")
        print(f"✅ SVG guardado en: {os.path.abspath(out_svg_path)}")
        plt.close()
        
        return out_svg_path
    
    def graf_base3_sql (DB_FILE,OUT_SVG):
        SQL_DUMP = "Base3_Ventas.sql"

        if os.path.exists(DB_FILE):
            conn = sqlite3.connect(DB_FILE)
        else:
            conn = sqlite3.connect(":memory:")
            if os.path.exists(SQL_DUMP):
                with open(SQL_DUMP, "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
            else:
                raise FileNotFoundError("No se encontró ni 'formas_pago.db' ni 'Base3_Ventas.sql'.")

        df = pd.read_sql_query("SELECT * FROM formas_pago", conn)
        conn.close()

        productos = ["premium", "magna", "diesel"]
        formas = ["efectivo", "debito", "credito"]

        totales = {prod: {f: df[f"{prod}_{f}"].sum() if f"{prod}_{f}" in df.columns else 0 for f in formas} for prod in productos}
        plot_df = pd.DataFrame(totales).T

        fig, ax = plt.subplots(figsize=(10, 6))
        bottom = [0]*len(plot_df)
        x = range(len(plot_df))

        colors = ["#4CAF50", "#FFC107", "#03A9F4"]

        for i, forma in enumerate(formas):
            vals = plot_df[forma].values
            bars = ax.bar(x, vals, bottom=bottom, color=colors[i], label=forma.capitalize())
            for bar, val in zip(bars, vals):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height()/2, 
                            f"{val:.0f}", ha="center", va="center", fontsize=8, color="black")
            bottom = [b + v for b, v in zip(bottom, vals)]

        ax.set_xticks(x)
        ax.set_xticklabels(plot_df.index.str.capitalize())
        ax.set_ylabel("Litros totales (mes)")
        ax.set_title("Distribución mensual por forma de pago y producto")
        ax.legend()
        ax.grid(True, axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()

        # Construir ruta completa en assets
        out_svg_path = os.path.join(ASSETS_DIR, OUT_SVG)

        plt.savefig(out_svg_path, format="svg")
        print(f"SVG guardado en: {os.path.abspath(out_svg_path)}")
        plt.close()

        return out_svg_path
    
    def graf_base4_json (JSON_FILE,OUT_SVG):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)

        meds = pd.json_normalize(raw.get("mediciones", []))
        meds["fecha"] = pd.to_datetime(meds["fecha"])
        # Asegurar columna fecha como datetime
        if "fecha" in meds.columns:
            meds["fecha"] = pd.to_datetime(meds["fecha"])

        meds = meds.sort_values("fecha").set_index("fecha")

        # Series a graficar
        benceno = meds["benceno_ppm"]
        co = meds["co_ppm"]

        fig, ax1 = plt.subplots(figsize=(11,6))
        ax1.plot(benceno.index, benceno.values, color="black", label="Benceno (ppm)", linewidth=1.5)
        ax1.set_ylabel("Benceno (ppm)", color="black")
        ax1.tick_params(axis='y', labelcolor="black")

        ax2 = ax1.twinx()
        ax2.plot(co.index, co.values, color="red", linestyle='--', label="CO (ppm)", linewidth=1.5)
        ax2.set_ylabel("CO (ppm)", color="red")
        ax2.tick_params(axis='y', labelcolor="red")

        ax1.set_ylim(-0.2, 0.3)
        ax2.set_ylim(1, 2.5)
        ax1.set_xlabel("Fecha")
        ax1.set_xticks(meds.index)
        ax1.set_xticklabels(meds.index.strftime("%Y-%m-%d"), rotation=90)

        # Leyenda combinada
        ax1.grid(True, linestyle="--", alpha=0.6)
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

        plt.title("Comparación Benceno vs CO (ppm) — Diario")
        plt.tight_layout()

        # Construir ruta completa en assets
        out_svg_path = os.path.join(ASSETS_DIR, OUT_SVG)

        plt.savefig(out_svg_path, format="svg")
        print(f"SVG guardado en: {os.path.abspath(out_svg_path)}")
        plt.close()

        return out_svg_path