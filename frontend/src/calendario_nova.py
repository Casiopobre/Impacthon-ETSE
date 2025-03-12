import locale
import flet as ft
from datetime import datetime
import calendar

# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'
COLOR_FILL = '#5FAAD9'
COLOR_BG_SEC = '#456173'

class Calendario:

    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Calendario'
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"
        self.page.padding = 20

        self.current_date = datetime.now()
        self.CALENDAR_HEADER = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

        self.header_text = ft.Text(size=20, weight="bold", text_align="center")
        self.calendar_grid = ft.GridView(
            expand=1,
            runs_count=7, # Columnas
            max_extent=50,
            child_aspect_ratio=1, # Relacion de aspecto
            spacing=5,
            run_spacing=5,
        )

        self._build_ui()
        self.update_calendar()

    def _build_ui(self):
        navigation_row = ft.Row(
            [
                ft.IconButton(ft.icons.ARROW_BACK, on_click=self.prev_month),
                self.header_text,
                ft.IconButton(ft.icons.ARROW_FORWARD, on_click=self.next_month),
            ],
            alignment="center"
        )
        
        calendar_container = ft.Container(
            content=self.calendar_grid,
            padding=5,
            border=ft.border.all(1, COLOR_BORDER),
            border_radius=5,
        )
        
        self.page.add(navigation_row, calendar_container)

    def update_calendar(self):
        self.header_text.value = self.current_date.strftime("%B %Y")
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        self.calendar_grid.controls.clear()

        for day in self.CALENDAR_HEADER:
            self.calendar_grid.controls.append(
                ft.Container(
                    content=ft.Text(day, weight="bold", text_align="center"),
                    alignment=ft.alignment.center,
                    padding=5,
                    border=ft.border.all(1, COLOR_BORDER)
                    
                )
            )

        for week in cal:
            for day in week:
                day_text = (str)(day) if day != 0 else ""
                bg_color = COLOR_BG if day != 0 else ft.colors.GREY
                self.calendar_grid.controls.append(
                    ft.Container(
                        content=ft.Text(day_text, text_align="center"),
                        alignment=ft.alignment.center,
                        padding=5,
                        bgcolor=bg_color,
                        border=ft.border.all(1, COLOR_BORDER),
                        border_radius=5
                    )
                )
        
        self.page.update()

    def prev_month(self, e):
        new_month = self.current_date.month - 1
        new_year = self.current_date.year
        if new_month < 1:
            new_month = 12
            new_year -= 1
        self.current_date = self.current_date.replace(year=new_year, month=new_month)
        self.update_calendar()

    def next_month(self, e):
        new_month = self.current_date.month + 1
        new_year = self.current_date.year
        if new_month > 12:
            new_month = 1
            new_year += 1
        self.current_date = self.current_date.replace(year=new_year, month=new_month)
        self.update_calendar()

def main(page: ft.Page):
    Calendario(page)

ft.app(target=main)

    