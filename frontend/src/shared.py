import flet as ft
SERVER_IP = "143.47.54.76"

SERGAS_1_HEX = "#034C8C"
SERGAS_2_HEX = "#5FAAD9"
SERGAS_3_HEX = "#456173"
SERGAS_4_HEX = "#048ABF"
SERGAS_5_HEX = "#F2F2F2"

SERGAS_1_RGBA = "rgba(3, 76, 140, 1)"
SERGAS_2_RGBA = "rgba(95, 170, 217, 1)"
SERGAS_3_RGBA = "rgba(69, 97, 115, 1)"
SERGAS_4_RGBA = "rgba(4, 138, 191, 1)"
SERGAS_5_RGBA = "rgba(242, 242, 242, 1)"

SERGAS_1_HSLA = "hsla(208, 95, 28, 1)"
SERGAS_2_HSLA = "hsla(203, 61, 61, 1)"
SERGAS_3_HSLA = "hsla(203, 25, 36, 1)"
SERGAS_4_HSLA = "hsla(197, 95, 38, 1)"
SERGAS_5_HSLA = "hsla(0, 0, 94, 1)"


def logout(page: ft.Page):
    page.client_storage.clear()
    page.launch_url = "/session/login"
    page.go("/session/login")