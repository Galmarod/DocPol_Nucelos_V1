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



import streamlit as st
import threading
from common.gral import General  
from __init__ import Docpol  


def Main():
    proyecto = Docpol()
    #st.title("Test Docpol")
    #proyecto.save_Bitacora()
    #proyecto.remplace()
    #proyecto.apitest()
    # Arrancar la API en un hilo (no bloqueante)
    proyecto.apitest()
    #proyecto.remplace()
    

if __name__ == "__main__":
    Main()



