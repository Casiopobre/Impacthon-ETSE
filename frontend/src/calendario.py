import flet as ft
import datetime
import calendar
from calendar import HTMLCalendar
from dateutil import relativedelta

'''
Basado en una clase creada por:
C. Nichols <mohawke@gmail.com>
'''

# Colors

class Calendar():

    def __init__(self, page):
        super().__init__()

        self.page = page
        self.get_current_date()
        self.set_theme()

        self.calendar_container = ft.Container(
            width=350, height=300, 
            padding=ft.padding.all(2), 
            border=ft.border.all(2, self.border_color),
            border_radius=ft.border_radius.all(5),
            alignment=ft.alignment.bottom_center
            )
        
        self.build()
        self.output=ft.Text() # Selected date

    def get_current_date(self):
        today = datetime.date.today()
        self.current_day = today.day
        self.current_month = today.month
        self.current_year = today.year

            
    def set_theme(self, border_color, text_color, curr_day_color):
        self.border_color = border_color
        self.text_color = text_color
        self.curr_day_color = curr_day_color

    def get_calendar(self):
        return HTMLCalendar().monthdayscalendar(self.current_year, self.current_month)
    
    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.build()
        self.calendar_container.update()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.build()
        self.calendar_container.update()

    def select_day(self, event):
        self.output.value = event.control.data
        self.output.update()

    def build(self):
        curr_calendar = self.get_calendar()
        str_date = f"{self.current_day} de {self.current_month} de {self.current_year}"
        date_display = ft.Text(str_date, text_align='center', size=20, color=self.text_color)
        
        next_button = ft.Button(
            ft.Text('>', size=20, color=self.text_color),
            on_click=self.next_month()
        )

        prev_button = ft.Button(
            ft.Text('<', size=20, color=self.text_color),
            on_click=self.prev_month()
        )

        # Div between the header and the calendar
        div = ft.Divider(height=1,thickness=2.0 , color=self.border_color)

        column = ft.Column(
            [ft.Row([prev_button, date_display, next_button],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=40,
            expand=False),
            div],
            spacing=2,
            width=350,
            height=330,
            alignment=ft.MainAxisAlignment.START,
            expand=False
        )

        for week in curr_calendar:
            row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day)

                    if len(display_day) == 1:
                        display_day = f"0{display_day}"
                    
                    if day == self.current_day:
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.curr_day_color
                    
                    day_button = ft.Container(
                        content=ft.Text(display_day, weight=is_current_day_font, color=self.text_color),
                        on_click=self.select_day,
                        data=(day, self.current_month, self.current_year),
                        width=40,
                        height=40,
                        ink=True,
                        alignment=ft.alignment.CENTER,
                        border_radius=ft.border_radius.all(5),
                        bgcolor=is_current_day_bg
                    )
                else:
                    day_button = ft.Container(
                        width=40, height=40, 
                        border_radius=ft.border_radius.all(5)
                    )

                row.controls.append(day_button)
            column.controls.append(row)
        self.calendar_container.content = column

        return self.calendar_container

