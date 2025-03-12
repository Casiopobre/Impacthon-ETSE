import flet as ft
import cipher as cp
import datetime
import requests
from calendario_nova import Calendario

SERVER_IP = "143.47.54.76"

# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'


def main(page: ft.Page):
    page.title = "Mi App con Calendario"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 20

    # Crear el calendario
    calendar = Calendario(page)  # Instancia el calendario

    # Menú lateral
    menu = ft.Column(
        controls=[
            ft.Text("Menú", size=20, weight="bold"),
            ft.ElevatedButton("Opción 1", on_click=lambda e: print("Opción 1")),
            ft.ElevatedButton("Opción 2", on_click=lambda e: print("Opción 2")),
        ],
        spacing=10,
    )

    # Diseño principal
    page.add(
        ft.Row(
            [
                menu,  # Menú lateral
                ft.VerticalDivider(width=10, color=ft.colors.GREY),  # Separador
                calendar.calendar_grid,  # Calendario (accedemos al GridView)
            ],
            expand=True,
        )
    )

ft.app(target=main)

