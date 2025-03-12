import flet as ft
import cipher as cp
import datetime
import requests
from calendario_nova import FletCalendar

SERVER_IP = "143.47.54.76"

# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'


def main(page: ft.Page):
    page.theme = ft.theme.Theme(color_scheme_seed=ft.colors.PINK)
    page.dark_theme = ft.theme.Theme(color_scheme_seed=ft.colors.PINK)

    # Instancia del calendario
    mycal = FletCalendar(page)

    # Agregar el calendario a la página
    page.add(mycal, mycal.output)
    page.update()


ft.app(
    target = main,
    #view = ft.WEB_BROWSER,
)
