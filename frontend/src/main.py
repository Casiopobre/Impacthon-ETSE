import flet as ft
import cipher as cp
import datetime
import requests
from calendario import Calendario

SERVER_IP = "143.47.54.76"

# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'


def main(page: ft.Page):
    page.title = "alendario"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 20

    # Crear el calendario
    calendar = Calendario(page)  # Instancia el calendario

    

ft.app(target=main)

