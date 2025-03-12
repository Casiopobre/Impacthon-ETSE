import locale
import flet as ft
from datetime import datetime
import calendar

# Configuracion do idioma
locale.setlocale(locale.LC_ALL, '')
# locale.setlocale(locale.LC_TIME, 'es_ES')  # Para Windows


# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'
COLOR_CURR_DAY = '#95C1DA'
COLOR_BG_SEC = '#456173'
COLOR_TEXT = '#000000'


class Calendario:

    def __init__(self):
        self.current_date = datetime.now()
        self.CALENDAR_HEADER = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

        self.header_text = ft.Text(size=20, weight="bold", text_align="center")
        self.calendar_grid = ft.GridView(
            expand=False,
            runs_count=7, # Columnas
            max_extent=50,
            child_aspect_ratio=1, # Relacion de aspecto
            spacing=5,
            run_spacing=5,
            width=7 * 50 + 6 * 5 
        )

        self._build_ui()
        self.update_calendar()

    def _build_ui(self):
        self.navigation_row = ft.Row(
            [
                ft.IconButton(ft.icons.ARROW_BACK, on_click=self.prev_month),
                self.header_text,
                ft.IconButton(ft.icons.ARROW_FORWARD, on_click=self.next_month),
            ],
            alignment="center"
        )
        
        self.calendar_container = ft.Container(
            content=self.calendar_grid,
            expand=False,
            padding=5,
            border=ft.border.all(2, COLOR_BORDER),
            border_radius=5,
            bgcolor=COLOR_BG,
            width=7 * 50 + 6 * 5  
        )
        
    def get_calendar_view(self):
        return self.calendar_container

    def update_calendar(self):
        self.header_text.value = self.current_date.strftime("%B %Y")
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        self.calendar_grid.controls.clear()

        for day in self.CALENDAR_HEADER:
            self.calendar_grid.controls.append(
                ft.Container(
                    content=ft.Text(day, weight="bold", text_align="center", color=COLOR_BG),
                    alignment=ft.alignment.center,
                    padding=5,
                    border_radius=5,
                    border=ft.border.all(1, COLOR_BORDER),
                    bgcolor=COLOR_BORDER
                )
            )

        for week in cal:
            for day in week:
                day_text = (str)(day) if day != 0 else ""
                bg_color = self.get_day_bg_color(day)

                self.calendar_grid.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(day_text, text_align="center", color=COLOR_TEXT, weight="bold"),
                                ft.Container(height=10)
                            ],
                            alignment=ft.alignment.center,
                            spacing=0
                        ),
                        alignment=ft.alignment.top_center,
                        padding=5,
                        bgcolor=bg_color,
                        border=ft.border.all(1, COLOR_BORDER),
                        border_radius=5
                    )
                )
        
        self.header_text.update()
        self.calendar_grid.update()
        #self.page.update()

    def get_day_bg_color(self, day):
        today = datetime.now().day
        this_month = datetime.now().month
        this_year = datetime.now().year

        if (
            day != 0 and 
            self.current_date.year == this_year and 
            self.current_date.month == this_month and 
            day == today
        ):
            return COLOR_CURR_DAY  # Color diferente para el día actual
        return COLOR_BG if day != 0 else COLOR_BG_SEC

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



    