import flet as ft
import homeM_funcs as hf
import homeM_funcs as hpf
import shared
from calendario import Calendario

def GestionarPacienteTab(page):
    codigo_field = ft.TextField(label="Codigo del Paciente", width=280)
    gestionar_button = ft.ElevatedButton(
            text="Gestionar Paciente", 
            width=200,
            on_click=lambda e: hf.gestionar_paciente( page, codigo_field.value )
            )
    qr_button = ft.IconButton(icon=ft.icons.ACCESS_ALARM, width=70)
    return ft.Column(
        [
            codigo_field,
            ft.Row(
                [
                    gestionar_button,
                    qr_button
                ],
                alignment= ft.MainAxisAlignment.CENTER
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )





def AnadirPacienteTab(page):
    name_field = ft.TextField(label="Nombre Completo", width=280)
    dni_field = ft.TextField(label="DNI", width=280)
    birth_field = ft.TextField(label="Fecha nacimiento", width=280)
    phone_field = ft.TextField(label="Número teléfono", width=280)
    password_field = ft.TextField(label="Contraseña", password=True, width=280)
    password_confirmation_field = ft.TextField(label="Confirmar Contraseña", password=True, width=280)


    def show_registration_dialog(page, password, code_text):
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
        
        code_display = ft.Container(
            content=ft.Text(
                f"Contraseña: {password}",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            margin=ft.margin.only(top=20, bottom=20),
            alignment=ft.alignment.center,
        )
        
        # Create text display for code
        pwd_display = ft.Container(
            content=ft.Text(
                f"Contraseña: {code_text}",
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
                ft.Text("Información de acceso", weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    on_click=lambda e: close_dialog(e, dialog, page)
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Column([
                qr_placeholder,
                code_display,
                pwd_display,
                ft.Text(
                    "Guarde esta contraseña para acceder a la aplicación",
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                    color=ft.colors.GREY_700,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        def close_dialog(e, dialog, page):
            dialog.open = False
            page.update()
        
        # Show the dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()



    def register_return(page: ft.Page):
        worked = hf.register_user(page, dni_field=dni_field, fecha_nac_field=birth_field, name_field=name_field, num_tlf_field=phone_field)
        print("worked")
        print(worked)
        print("worked")
        print("worked")
        if worked[0]:
            show_registration_dialog(page, worked[1], worked[2])


    register_button = ft.ElevatedButton(
        text="Dar de alta",
        icon=ft.icons.QR_CODE,
        on_click=lambda e: register_return(page)

    )

    return ft.Row (
        [ft.Column(
            [
                name_field,
                dni_field,
                birth_field,
                phone_field,
                password_field,
                password_confirmation_field,
                register_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

def build_homeM_view(page: ft.Page):
    """
    Construye la vista principal del paciente con la lista de medicamentos y espacio para el calendario.
    """
    page.title = "Título genérico"
    
    profile_name = "Médico"  # This would come from actual user data
    Vis = ft.Container()
    
    if (page.route == "/homem/ges"):
        Vis.content = GestionarPacienteTab(page)
    elif (page.route == "/homem/an"):
        Vis.content=AnadirPacienteTab(page)


    def GestionClick(e):
        page.go("/homem/ges")
    def AnadirClick(e):
        page.go("/homem/an")

    estilo = ft.ButtonStyle(color=ft.colors.WHITE)
    boton_ges = ft.TextButton(text="Gestionar Paciente",style=estilo,on_click= GestionClick)
    boton_an = ft.TextButton(text="Añadir Pacientes",style=estilo, on_click= AnadirClick)
    nav_bar = ft.Row(
        controls=[
            boton_ges,
            boton_an,
            ft.PopupMenuButton(
                icon=ft.icons.DOUBLE_ARROW,
                icon_color=ft.colors.WHITE,
                tooltip="Cambiar perfil",
                items = [
                    ft.PopupMenuItem(text = "Cerrar Sesion", on_click=lambda e: shared.logout(page)),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(text="Ajustes")
                ]
            ),
            # ft.Spacer(),
            ft.Text(profile_name, color=ft.colors.WHITE, size=16),
            ft.Container(
                content=ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30, color=ft.colors.WHITE),
                margin=ft.margin.only(left=10)
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


    # Update layout when window size changes
    page.on_resize = lambda _: page.update()
    # Main view
    return ft.View(
        route= page.route,
        controls=[
            # AppBar with navigation
            ft.AppBar(
                bgcolor=shared.SERGAS_1_HEX,
                actions=[nav_bar],
            ),
            Vis
        ],
    )



def GestionarPacienteObtenido(page, id_paciente):
    """Builds the patient data management view for medical professionals."""
    # Mock patient data - replace with actual API calls
    
    nombre = hf.temp_patient_data[id_paciente].get("nombre")
    fecha_nacimiento = hf.temp_patient_data[id_paciente].get("fecha_nacimiento")
    dni = hf.temp_patient_data[id_paciente].get("dni")
    email = hf.temp_patient_data[id_paciente].get("email")
    num_tlf = hf.temp_patient_data[id_paciente].get("numTlf")
    edad = hf.calculate_age(fecha_nacimiento.split(" ")[0])
     
    
    medications = hf.get_paciente_recetas(page, id_paciente)
    
    # Function to handle medication deletion
    def delete_medication(e, med_id):
        # API call would go here
        page.snack_bar = ft.SnackBar(ft.Text(f"Eliminando medicamento ID: {med_id}"))
        page.snack_bar.open = True
        page.update()
    
    # Function to handle adding new medication
    def add_medication(e):
        page.snack_bar = ft.SnackBar(ft.Text("Función para añadir medicamento"))
        page.snack_bar.open = True
        page.update()
    
    # Function to handle patient data modification
    def modify_patient(e):
        page.snack_bar = ft.SnackBar(ft.Text("Modificando datos del paciente"))
        page.snack_bar.open = True
        page.update()
    
    # Patient profile card
    profile_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"{nombre}", 
                            weight=ft.FontWeight.BOLD, 
                            size=20),
                    ft.Divider(),
                    ft.Text(f"DNI: {dni}"),
                    ft.Text(f"Edad: {edad} años"),
                    ft.Text(f"Fecha nacimiento: {fecha_nacimiento}"),
                    ft.Text(f"Teléfono: {num_tlf}"),
                    ft.Container(height=20),  # Spacer
                    ft.ElevatedButton(
                        "Modificar datos",
                        icon=ft.icons.EDIT,
                        on_click=modify_patient,
                        width=200
                    )
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=5,
            width=300
        ),
        elevation=4
    )
    
    # Calendar placeholder
    calendario = Calendario(page)

    calendar_container = ft.Container(
        content=(
            ft.Column(
                [
                    ft.Row(
                        [
                            calendario.navigation_row
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        
                    ),
                    calendario.get_calendar_view()
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        ),
        padding=20,
        expand=False,
        width=400
    )
    calendar_placeholder = ft.Container(
        content=ft.Column(
            controls=[
                calendar_container,
                ft.Container(
                    content=ft.Text("Calendario de recetas del paciente",
                                   text_align=ft.TextAlign.CENTER),
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=8,
                    padding=10,
                    height=190,
                    width=400,
                    alignment=ft.alignment.center
                )
            ],
            spacing=5
        ),
        margin=ft.margin.only(top=20),
        width=400
    )
    
    # Left column with profile and calendar
    left_column = ft.Column(
        controls=[
            profile_card,
            calendar_placeholder
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Create medication list items with delete buttons
    medication_items = []
    for med in medications:
        medication_items.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(med["name"], weight=ft.FontWeight.BOLD),
                                ft.Text(f"Dosificación: {med['dose']}"),
                                ft.Text(f"Intervalo: Cada {med['interval']} horas"),
                                ft.Text(f"Fecha fin: {med['end_date']}")
                            ],
                            spacing=5,
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.colors.RED_600,
                            tooltip="Eliminar medicación",
                            on_click=lambda e: delete_medication(e)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(bottom=10)
            )
        )
    
    # Medication container
    medication_container = ft.Container(
        content=ft.Column(
            controls=[
                # Add medication button row
                ft.Row(
                    controls=[
                        ft.Text("Medicaciones", weight=ft.FontWeight.BOLD, size=18),
                        ft.ElevatedButton(
                            "Añadir medicación",
                            icon=ft.icons.ADD,
                            on_click=add_medication
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(),
                # Medication list
                ft.Column(
                    controls=medication_items,
                    spacing=5,
                    scroll=ft.ScrollMode.AUTO
                ) if medication_items else ft.Text("No hay medicaciones registradas")
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=20,
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=5,
        expand=True
    )
    
    # Main content
    content = ft.Row(
        controls=[
            left_column,
            ft.VerticalDivider(width=1),
            medication_container
        ],
        spacing=20,
        expand=True
    )
    
    # Return the view
    return ft.View(
        route=f"/homem/ges/{id_paciente}",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Gestión de Paciente {id_paciente}"),
                bgcolor=shared.SERGAS_1_HSLA,
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: page.go("/homem/ges")
                    )
                ]
            ),
            ft.Container(
                content=content,
                padding=20,
                expand=True
            )
        ]
    )
