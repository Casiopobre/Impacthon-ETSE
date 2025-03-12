import flet as ft
import datetime
import calendar

# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'


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

