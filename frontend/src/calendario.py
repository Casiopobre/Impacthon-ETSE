import locale
import flet as ft
from datetime import datetime
import calendar

# Configuración del idioma
locale.setlocale(locale.LC_ALL, '')  # Ajusta automáticamente al idioma del sistema
# locale.setlocale(locale.LC_TIME, 'es_ES')  # Descomentar para forzar español en Windows

# Colores
COLOR_BG = '#F2F2F2'
COLOR_BORDER = '#034C8C'
COLOR_CURR_DAY = '#95C1DA'
COLOR_BG_SEC = '#456173'
COLOR_TEXT = '#000000'


class Calendario:
    def __init__(self, page: ft.Page):
        self.current_date = datetime.now()
        self.CALENDAR_HEADER = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        self.page = page
        self.daily_data = {}
        self.header_text = ft.Text(size=20, weight="bold", text_align="center")
        self.calendar_grid = ft.GridView(
            expand=False,
            runs_count=7,  # Número de columnas
            max_extent=50,
            child_aspect_ratio=1,  # Relación de aspecto
            spacing=5,
            run_spacing=5,
            width=7 * 50 + 6 * 5
        )

        self._build_ui()
        self.update_calendar()
        self.page.add(self.navigation_row, self.calendar_container)

    def add_symptom(self, date, symptom):
        if date not in self.daily_data:
            self.daily_data[date] = {"symptoms": [], "medications": []}
        self.daily_data[date]["symptoms"].append(symptom)

    def add_medication(self, date, medication):
        if date not in self.daily_data:
            self.daily_data[date] = {"symptoms": [], "medications": []}
        self.daily_data[date]["medications"].append(medication)

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

    def update_calendar(self):
        self.header_text.value = self.current_date.strftime("%B %Y").capitalize()
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        self.calendar_grid.controls.clear()

        # Agregar encabezado de días de la semana
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

        # Agregar los días del mes
        for week in cal:
            for day in week:
                day_text = (str)(day) if day != 0 else ""
                date_key = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                bg_color = self.get_day_bg_color(day)

                symptoms = ", ".join(self.daily_data.get(date_key, {}).get("symptoms", []))
                medications = ", ".join(self.daily_data.get(date_key, {}).get("medications", []))

                day_content = ft.Column(
                    [
                        ft.Text(day_text, text_align="center", color=COLOR_TEXT, weight="bold"),
                        ft.Text(f"Symptoms {symptoms}" if symptoms else "", size=10, color=ft.colors.RED_500),
                        ft.Text(f"Medications {medications}" if medications else "", size=10, color=ft.colors.BLUE_500)
                    ],
                    alignment=ft.alignment.center,
                    spacing=2
                )

                self.calendar_grid.controls.append(
                    ft.Container(
                        content=day_content,
                        alignment=ft.alignment.top_center,
                        padding=5,
                        bgcolor=self.get_day_bg_color(day),
                        border=ft.border.all(1, COLOR_BORDER),
                        border_radius=5,
                        on_click=lambda e, d=date_key: self.open_day_details(d)
                    )
                )
        
        #self.header_text.update()
        #self.calendar_grid.update()
        self.page.update()

    def open_day_details(self, date_key):
        symptoms_input = ft.TextField(label="Síntoma")
        medication_input = ft.TextField(label="Medicamento")

        def save_data(e):
            if symptoms_input.value:
                self.add_symptom(date_key, symptoms_input.value)
            if medication_input.value:
                self.add_medication(date_key, medication_input.value)
            
            dialog.open = False
            self.update_calendar()
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Registrar datos para {date_key}"),
            content=ft.Column([
                symptoms_input,
                medication_input
            ], tight=True),
            actions=[
                ft.ElevatedButton("Cancelar", on_click=lambda e: setattr(dialog, "open", False)),
                ft.ElevatedButton("Guardar", on_click=save_data)
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def get_day_bg_color(self, day):
        today = datetime.now()
        if (
            day != 0 and
            self.current_date.year == today.year and
            self.current_date.month == today.month and
            day == today.day
        ):
            return COLOR_CURR_DAY  # Color para el día actual
        return COLOR_BG if day != 0 else COLOR_BG_SEC

    def prev_month(self, e):
        self.current_date = self.current_date.replace(
            year=self.current_date.year - 1 if self.current_date.month == 1 else self.current_date.year,
            month=12 if self.current_date.month == 1 else self.current_date.month - 1
        )
        self.update_calendar()
    def get_calendar_view(self):
        return self.calendar_container
    def next_month(self, e):
        self.current_date = self.current_date.replace(
            year=self.current_date.year + 1 if self.current_date.month == 12 else self.current_date.year,
            month=1 if self.current_date.month == 12 else self.current_date.month + 1
        )
        self.update_calendar()
