#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Guillermo Almazán Rodríguez"
__copyright__  = "Copyright 2024, RevelCode"
__credits__    = ["galmarod"]
__license__    = "GPL"
__version__    = "1.0.1"
__maintainer__ = "Francisco Javier Mendoza Bautista"
__email__      = "javimenba.developer@gmail.com"
__status__     = "Development"
__date__       = "Oct-2024"


import functools
import time

def manejar_excepciones(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Asumiendo que 'self' es el primer argumento
            self = args[0]
            self.logger.error(f"Error en {func.__name__}: {e}", exc_info=True)
            # Opcional: re-raise la excepción si deseas que se propague
            # raise
    return wrapper

def registrar_actividad(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.logger.info(f"Iniciando {func.__name__}")
        resultado = func(*args, **kwargs)
        self.logger.info(f"Finalizado {func.__name__}")
        return resultado
    return wrapper

def medir_tiempo(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        tiempo_transcurrido = fin - inicio
        self.logger.info(f"{func.__name__} tomó {tiempo_transcurrido:.4f} segundos")
        return resultado
    return wrapper
