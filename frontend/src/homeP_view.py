import flet as ft
import session_funcs as sf
import shared
from calendario import Calendario

def build_homeP_view(page: ft.Page):
    """
    Construye la vista principal del paciente con la lista de medicamentos y espacio para el calendario.
    """
    page.title = "Mi Medicación"
    
    # Función para abrir el menú de síntomas
    def open_symptom_menu(e):
        page.go("/sintomas")
        page.update()

    # Botón para el menú de síntomas
    symptoms_button = ft.ElevatedButton(
        "Menú de Síntomas",
        icon=ft.icons.HEALTH_AND_SAFETY,
        on_click=open_symptom_menu,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10), 
            padding=ft.padding.all(25),
            text_style=ft.TextStyle(size=24)  # Aumenta el tamaño del texto
        ),
        width=500,
        height=70,
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
    calendario = Calendario(page)

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
            ft.AppBar(title=ft.Text("Mi Medicación"), bgcolor='#95C1DA'),
            ft.Container(content=buttons_container, padding=ft.padding.only(top=20, bottom=10)),
            #medication_list,
            get_content_layout(),
        ],
    )
    
def build_symptom_menu_view(page: ft.Page):
    def on_sintoma_selected(e):
        if e.control.content.controls[1].value == "Más opciones":
            # Mostrar el cuadro de diálogo para ingresar síntomas y medicamentos
            open_symtoms_details(page)  # Llamar a open_symtoms_details para mostrar el diálogo
        else:
            print(f"{e.control.content.controls[1].value} seleccionado")
            page.go("/homep")

    def create_sintoma_button(text, image_path):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Image(src=f"/{image_path}", width=80, height=80), 
                    ft.Text(text, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),  # Texto
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=150,  # Tamaño del botón
            height=150,
            alignment=ft.alignment.center,
            bgcolor='#95C1DA',  # Color de fondo
            border_radius=10,  # Bordes redondeados
            on_click=on_sintoma_selected,  # Acción cuando se presiona
            padding=10
        )

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
                    create_sintoma_button("Mareos", "icono_mareo.svg"),
                    create_sintoma_button("Más opciones", "icono_opcionMas.svg")
                ],
                max_extent=160,
                spacing=10,
                run_spacing=10,
            )
        ],
    )

def open_symtoms_details(page: ft.Page):
    # Crear los campos de entrada para los síntomas y medicamentos
    symptoms_input = ft.TextField(label="Síntoma")

    # Función para cerrar el diálogo
    def cerrar(e):
        dialog.open = False
        page.update()

    # Función para guardar los datos
    def save_data(e):
        if symptoms_input.value:
            print(f"Síntoma: {symptoms_input.value}")  # Puedes procesar el síntoma aquí

        dialog.open = False
        # Navegar de vuelta a la vista principal (home)
        page.go("/homep")
        page.update()

    # Crear el diálogo con los campos de entrada
    dialog = ft.AlertDialog(
        title=ft.Text("Registrar síntoma"),
        content=ft.Column([
            symptoms_input,
        ], tight=True),
        actions=[
            ft.ElevatedButton("Cancelar", on_click=cerrar),
            ft.ElevatedButton("Guardar", on_click=save_data)
        ],
    )

    # Mostrar el diálogo
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def route_change(page: ft.Page):
    """
    Maneja la navegación entre las diferentes vistas.
    """
    page.views.clear()

    if page.route == "/home":
        page.views.append(build_homeP_view(page))
    elif page.route == "/sintomas":
        page.views.append(build_symptom_menu_view(page))

    page.update()


if __name__ == "__main__":
    ft.app(target=route_change)
