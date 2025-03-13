import flet as ft
import session_funcs as sf
import homeP_funcs as hpf
import shared
from calendario import Calendario

def build_homeP_view(page: ft.Page):
    """
    Construye la vista principal del paciente con la lista de medicamentos y espacio para el calendario.
    """
    page.title = "Mi Medicación"
    
    # Función para abrir el cuadro de diálogo de sentimientos
    # def open_feeling_dialog(e):
    #     feeling_dialog = ft.AlertDialog(
    #         title=ft.Text("¿Cómo te sientes?"),
    #         content=ft.Column([
    #             ft.TextField(label="Describe cómo te sientes")
    #         ], tight=True, spacing=20),
    #         actions=[
    #             ft.ElevatedButton("Cancelar", on_click=lambda e: setattr(feeling_dialog, "open", False)),
    #             ft.ElevatedButton("Enviar", on_click=lambda e: setattr(feeling_dialog, "open", False))
    #         ]
    #     )
    #     page.dialog = feeling_dialog
    #     feeling_dialog.open = True
    #     page.update()
    
    # Botón para ir al menú de síntomas
    def open_symptom_menu(e):
        page.go("/homep/sintomas")
        page.update()

    # Botón de sentimifentos
    # feeling_button = ft.ElevatedButton(
    #     "¿Cómo te sientes?",
    #     icon=ft.icons.MOOD,
    #     on_click=open_symptom_menu,
    #     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.all(15)),
    # )

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
        return hpf.get_user_medications(page)


    def create_medication_card(medication):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row(
                        [
                        ft.Icon(ft.icons.MEDICATION, size=40, color=ft.colors.BLUE_400),
                        ft.Column(
                            [
                                ft.Text(medication["name"], weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Dosis: {medication['dose']} mg"),
                                ft.Text(f"Intervalo: Cada {medication['interval']} horas"),
                            ],
                            spacing=5,
                            wrap=True
                        ),
                        ]
                    ),
                    ft.Divider(height=10, thickness=1),
                    ft.Row([
                        ft.Text(f"Desde: {hpf.format_date(medication.get('start_date', ''))}"),
                        ft.Text(f"Hasta: {hpf.format_date(medication.get('end_date', ''))}"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                padding=15,
            ),
            margin=ft.margin.only(bottom=10),
        )


    medication_list = ft.ListView(
        spacing=10, padding=20, expand=True
    )
    medications = get_medication_data()
    
    if medications:
        for medication in medications:
            medication_list.controls.append(create_medication_card(medication))
    else:
        medication_list.controls.append(
            ft.Container(
                content=ft.Text("No hay medicamentos para mostrar", 
                                style=ft.TextStyle(italic=True)),
                alignment=ft.alignment.center,
                padding=20
            )
        )
        
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

    # Main content layout - separated in 2 rows for better adaptation
    def get_content_layout():
        # First row: Medication list with header
        medication_row = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Medicamentos de hoy", size=20, weight=ft.FontWeight.BOLD),
                    medication_list,
                ],
                spacing=10,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )

        # Second row: Calendar container
        calendar_row = ft.Container(
            content=calendar_container,
            padding=ft.padding.all(20),
            expand=False,
        )

        # Return as a column with 2 rows
        return ft.Column(
            controls=[
                medication_row,
                calendar_row,
            ],
            expand=True,
        )

    # Update layout when window size changes
    page.on_resize = lambda _: page.update()
    # Add this function before defining boton_codigo
    def show_code_dialog(page):
        # This will hold the text that would be received from server
        code_text = hpf.get_otp_key(page)
        
        # Create placeholder for future QR code implementation
        qr_placeholder = ft.Container(
            width=200,
            height=200,
            bgcolor=ft.colors.GREY_300,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.Icon(ft.icons.QR_CODE, size=100, color=ft.colors.GREY_800),
                ft.Text("QR Code Placeholder", color=ft.colors.GREY_800)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        
        # Create text display for code
        code_display = ft.Container(
            content=ft.Text(
                code_text,
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            margin=ft.margin.only(top=20, bottom=20),
            alignment=ft.alignment.center,
        )
        


        # Create the dialog
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Text("Mi Código de Acceso", weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.icons.CLOSE
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Column([
                qr_placeholder,
                code_display,
                ft.Text(
                    "Este código permite a los profesionales médicos acceder a tu información",
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                    color=ft.colors.GREY_700,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        print("--------")
        print("--------")
        print(code_text)
        print("--------")
        print("--------")
        
        # Show the dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
       
    boton_codigo = ft.ElevatedButton(
        text="Mi Código",
        icon=ft.icons.QR_CODE,
        on_click=lambda _: show_code_dialog(page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            color=shared.SERGAS_2_HEX,
            bgcolor=shared.SERGAS_1_HEX,
        )
    )
    profile_name = "Nombre generico"
    nav_bar = ft.Row(
        controls=[
            boton_codigo,
            ft.PopupMenuButton(
                icon=ft.icons.DOUBLE_ARROW,
                icon_color=shared.SERGAS_5_HEX,
                tooltip="Cambiar perfil",
                items = [
                    ft.PopupMenuItem(text = "Cerrar Sesion"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Ajustes")
                ]
            ),
            # ft.Spacer(),
            ft.Text(profile_name, color=shared.SERGAS_5_HEX, size=16),
            ft.Container(
                content=ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30, color=shared.SERGAS_5_HEX),
                margin=ft.margin.only(left=10)
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )




    # Main view
    return ft.View(
        route="/homep",
        controls=[
            ft.AppBar(
                title=ft.Text("Mi medicaciooooooooooooon"),
                bgcolor=ft.colors.DEEP_ORANGE_800,
                actions=[nav_bar],
                      ),
            ft.Container(content=buttons_container, padding=ft.padding.only(top=20, bottom=10)),
            #medication_list,
            get_content_layout(),
        ],
    )



def build_symptom_menu_view(page: ft.Page):
    """
    Construye la vista del menú de síntomas con opciones seleccionables.
    """
    page.title = "Menú de Síntomas"

    symptoms = [
        "Dolor de cabeza",
        "Fiebre",
        "Tos",
        "Cansancio",
        "Dolor muscular",
        "Náuseas",
        "Vómito",
        "Diarrea",
        "Estreñimiento",
        "Mareos",
        "Congestión nasal",
    ]

    symptom_checkboxes = [ft.Checkbox(label=s, value=False) for s in symptoms]

    def return_to_home(e):
        page.go("/home")
        page.update()

    return ft.View(
        route="homep/sintomas",
        controls=[
            ft.AppBar(title=ft.Text("Selecciona tus síntomas"), bgcolor=ft.colors.DEEP_ORANGE_800),
            ft.Column(symptom_checkboxes, spacing=10, padding=20),
            ft.ElevatedButton("Volver", icon=ft.icons.ARROW_BACK, on_click=return_to_home),
        ],
    )


def route_change(page: ft.Page):
    """
    Maneja la navegación entre las diferentes vistas.
    """
    page.views.clear()

    if page.route == "/home":
        page.views.append(build_homeP_view(page))
    elif page.route == "/homep/sintomas":
        page.views.append(build_symptom_menu_view(page))

    page.update()


if __name__ == "__main__":
    ft.app(target=route_change)
