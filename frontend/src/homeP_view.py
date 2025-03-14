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
    
    # Función para abrir el menú de síntomas
    def open_symptom_menu(e):
        page.go("/homep/sintomas")
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
    calendario = Calendario(page)
    if medications:
        for medication in medications:
            medication_list.controls.append(create_medication_card(medication))
    for medication1 in calendario.daily_data.get(calendario.current_date, {}).get("medications", []):
        medication_list.controls.append(create_medication_card(medication1))    
    else:
        medication_list.controls.append(
            ft.Container(
                content=ft.Text("No más hay medicamentos para mostrar", 
                                style=ft.TextStyle(italic=True)),
                alignment=ft.alignment.center,
                padding=20
            )
        )
        
    # Container for the calendar 

    calendar_container = ft.Container(
        content=(
            ft.Column(
                [
                    ft.Row(
                        [
                            calendario.navigation_row
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    calendario.get_calendar_view()
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ),
        padding=20,
        expand=False,
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
                scroll=ft.ScrollMode.AUTO,
                spacing=10,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )

        # Return as a column with 2 rows
        return ft.Row(
            controls=[
                medication_row,
                calendar_container,
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
    profile_name = "Paciente"
    nav_bar = ft.Row(
        controls=[
            boton_codigo,
            ft.PopupMenuButton(
                icon=ft.icons.DOUBLE_ARROW,
                icon_color=shared.SERGAS_5_HEX,
                tooltip="Cambiar perfil",
                items = [
                    ft.PopupMenuItem(text = "Cerrar Sesion", on_click=lambda _: shared.logout(page)),
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
                title=ft.Text("Mi medicacion"),
                bgcolor='#034C8C',
                actions=[nav_bar],
                      ),
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
        route="homep/sintomas",
        controls=[
            ft.AppBar(
                bgcolor=ft.colors.DEEP_ORANGE_800,
            ),
            ft.Text("Selecciona los síntomas que tienes hoy", size=20, weight=ft.FontWeight.BOLD),
            ft.GridView(
                controls=[   
                   
                    create_sintoma_button("Cansancio", "icono_cansancio.svg"),
                    create_sintoma_button("Congestión", "icono_congesion.svg"),
                    create_sintoma_button("Diarrea", "icono_diarrea.svg"),
                    create_sintoma_button("Dolor de cabeza", "icono_dolor_cabeza.svg"),
                    create_sintoma_button("Dolor muscular", "icono_dolor_muscular.svg"),
                    create_sintoma_button("Estreñimiento", "icono_estrenimiento.svg"),
                    create_sintoma_button("Fiebre", "icono_fiebre.svg"),
                    create_sintoma_button("Mareos", "icono_mareo.svg"),
                    create_sintoma_button("Náuseas", "icono_nauseas.svg"),
                    create_sintoma_button("Tos", "icono_tos.svg"),
                    create_sintoma_button("Vómito", "icono_vomito.svg"),
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
        page.go("/homep")
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
    elif page.route == "/homep/sintomas":
        page.views.append(build_symptom_menu_view(page))

    page.update()


if __name__ == "__main__":
    ft.app(target=route_change)
