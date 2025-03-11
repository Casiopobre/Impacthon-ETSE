import flet as ft
import cipher as cp
import requests


def main(page: ft.Page):
    page.title = "Basic Cipher/Decipher App"
    page.window_width = 640
    page.window_height = 480
    page.window_resizable = False
    page.padding = 48
    page.margin = 48

    def button_clicked(e):    
        texto.value=(requests.get("http://localhost:8080/test").json())
        page.update()

    botonTest=ft.TextButton(text="Text button", on_click=button_clicked)
    texto=ft.Text("Size 70, w900, selectable", size=70, weight=ft.FontWeight.W_900, selectable=True)


    page.add(
        texto,
        botonTest
    )


    

ft.app(
    target = main,
    #view = ft.WEB_BROWSER,
)
