import flet as ft
import session_funcs as sf
import shared
from calendario import Calendario
from datetime import datetime

def build_homeP_view(page: ft.Page, calendario: Calendario):
    """
    Construye la vista principal del paciente con la lista de medicamentos y espacio para el calendario.
    """
    page.title = "Mi Medicación"
    
    # Botón para ir al menú de síntomas
    def open_symptom_menu(e):
        page.go("/sintomas")
        page.update()

    # Botón para el menú de síntomas
    symptoms_button = ft.ElevatedButton(
        "Menú de Síntomas",
        icon=ft.icons.HEALTH_AND_SAFETY,
        on_click=open_symptom_menu,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.all(15)),
    )

    # Contenedor para botones en la parte superior
    buttons_container = ft.Row(
        controls=[symptoms_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Lista de medicamentos
    def get_medication_data():
        return [
            {"name": "Paracetamol", "dose": 500, "interval": 8},
            {"name": "Ibuprofeno", "dose": 400, "interval": 6},
            {"name": "Omeprazol", "dose": 20, "interval": 24},
            {"name": "Amoxicilina", "dose": 750, "interval": 12},
        ]

    def create_medication_card(medication):
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.MEDICATION, size=40, color=ft.colors.BLUE_400),
                        ft.Column(
                            [
                                ft.Text(medication["name"], weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Dosis: {medication['dose']} mg"),
                                ft.Text(f"Intervalo: Cada {medication['interval']} horas"),
                            ],
                            spacing=5,
                        ),
                    ]
                ),
                padding=15,
            ),
            margin=ft.margin.only(bottom=10),
        )

    medication_list = ft.ListView(
        spacing=10, padding=20, expand=True
    )
    
    for medication in get_medication_data():
        medication_list.controls.append(create_medication_card(medication))

    # Container for the calendar 
    calendar_container = ft.Container(
        content=(
            ft.Column(
                [
                    calendario.navigation_row, calendario.get_calendar_view()
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ),
        padding=20,
        expand=False
    )

    # Main content layout - responsive
    def get_content_layout():
        # Check if we're on mobile
        if page.width < 600:
            # Mobile layout: Calendar under medication list
            return ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Medicamentos de hoy", size=20, weight=ft.FontWeight.BOLD),
                                medication_list,
                            ],
                        ),
                        expand=True,
                    ),
                    calendar_container,
                ],
                expand=True,
            )
        else:
            # Desktop/web layout: Calendar to the right of medication list
            return ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Medicamentos de hoy", size=20, weight=ft.FontWeight.BOLD),
                                medication_list,
                            ],
                        ),
                        expand=True,
                    ),
                    calendar_container,
                ],
                expand=True,
            )

    # Update layout when window size changes
    page.on_resize = lambda _: page.update()

    # Main view
    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(title=ft.Text("Mi Medicación"), bgcolor=ft.colors.DEEP_ORANGE_800),
            ft.Container(content=buttons_container, padding=ft.padding.only(top=20, bottom=10)),
            #medication_list,
            get_content_layout(),
        ],
    )


# Función para construir la vista de síntomas
def build_sintomas_view(page: ft.Page, calendario: Calendario):
    def on_sintoma_selected(e):
        selected_date = calendario.current_date or datetime.now().date()
        calendario.add_symptom(selected_date, e.control.text)

        print(f"{e.control.text} añadido el {selected_date}")
        
        page.go("/homep")

    return ft.View(
        route="/sintomas",
        controls=[
            ft.AppBar(
                title=ft.Text("Síntomas"),
                bgcolor=ft.colors.DEEP_ORANGE_800,
            ),
            ft.Text("Selecciona los síntomas que tienes hoy", size=20, weight=ft.FontWeight.BOLD),
            ft.GridView(
                controls=[
                    ft.ElevatedButton("Dolor de cabeza", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Fiebre", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Tos", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Cansancio", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Dolor muscular", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Mareos", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Náuseas", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Vómito", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Diarrea", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Estreñimiento", on_click=on_sintoma_selected),
                    ft.ElevatedButton("Congestión nasal", on_click=on_sintoma_selected),
                ],
                max_extent=200,
                spacing=10,
                run_spacing=10,
            )
        ],
    )

