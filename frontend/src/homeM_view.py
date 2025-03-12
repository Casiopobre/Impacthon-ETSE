import flet as ft
import homeM_funcs as hf
import shared

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
    name_field = ft.TextField(label="Nombre completo", width=280)
    dni_field = ft.TextField(label="DNI", width=280)
    birth_field = ft.TextField(label="Fecha nacimiento", width=280)
    phone_field = ft.TextField(label="Número teléfono", width=280)
    password_field = ft.TextField(label="Contraseña", password=True, width=280)
    password_confirmation_field = ft.TextField(label="Confirmar Contraseña", password=True, width=280)

    register_button = ft.ElevatedButton(
        text="Registrarse",
        on_click=lambda e: hf.register_user(page, dni_field, birth_field, password_field, password_field, phone_field)
    )

    return ft.Column(
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

def build_homeM_view(page: ft.Page):
    """
    Construye la vista principal del paciente con la lista de medicamentos y espacio para el calendario.
    """
    page.title = "Título genérico"
    
    profile_name = "nombre"  # This would come from actual user data
    Vis = ft.Container()
    
    if (page.route == "/homem/ges"):
        Vis.content = GestionarPacienteTab(page)
    elif (page.route == "/homem/an"):
        Vis.content=AnadirPacienteTab(page)


    def GestionClick(e):
        page.go("/homem/ges")
    def AnadirClick(e):
        page.go("/homem/an")


    boton_ges = ft.TextButton(text="Gestionar Paciente",on_click= GestionClick)
    boton_an = ft.TextButton(text="Añadir Pacientes", on_click= AnadirClick)
    nav_bar = ft.Row(
        controls=[
            boton_ges,
            boton_an,
            ft.IconButton(
                icon=ft.icons.DOUBLE_ARROW,
                icon_color=ft.colors.WHITE,
                tooltip="Cambiar perfil",
                on_click=lambda e: print("Switch profile clicked")
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
                title=ft.Text("Home Page"),
                bgcolor=ft.colors.DEEP_ORANGE_800,
                actions=[nav_bar],
            ),
            Vis
        ],
    )
    
def GestionarPacienteObtenido(page, id_paciente):
    """Builds the patient data management view for medical professionals."""
    # Mock patient data - replace with actual API calls
    patient_data = {
        "id": id_paciente,
        "nombre": "Paciente Ejemplo",
        "edad": 45,
        "dni": "12345678X",
        "fecha_nacimiento": "1980-01-15",
        "num_tlf": "666123456"
    }
    
    # Mock medications - replace with actual API calls
    medications = [
        {"id": 1, "nombre": "Paracetamol", "dosificacion": "1 comprimido", 
         "fecha_fin": "2025-04-30", "intervalos_dosificacion": 8},
        {"id": 2, "nombre": "Ibuprofeno", "dosificacion": "2 comprimidos", 
         "fecha_fin": "2025-05-10", "intervalos_dosificacion": 12},
        {"id": 3, "nombre": "Omeprazol", "dosificacion": "1 cápsula", 
         "fecha_fin": "2025-06-15", "intervalos_dosificacion": 24}
    ]
    
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
                    ft.Text(f"{patient_data['nombre']}", 
                            weight=ft.FontWeight.BOLD, 
                            size=20),
                    ft.Divider(),
                    ft.Text(f"DNI: {patient_data['dni']}"),
                    ft.Text(f"Edad: {patient_data['edad']} años"),
                    ft.Text(f"Fecha nacimiento: {patient_data['fecha_nacimiento']}"),
                    ft.Text(f"Teléfono: {patient_data['num_tlf']}"),
                    ft.Container(height=20),  # Spacer
                    ft.ElevatedButton(
                        "Modificar datos",
                        icon=ft.icons.EDIT,
                        on_click=modify_patient,
                        width=200
                    )
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            width=300
        ),
        elevation=4
    )
    
    # Calendar placeholder
    calendar_placeholder = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Calendario", weight=ft.FontWeight.BOLD, size=16),
                ft.Container(
                    content=ft.Text("Calendario de recetas del paciente",
                                   text_align=ft.TextAlign.CENTER),
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=8,
                    padding=20,
                    height=200,
                    width=300,
                    alignment=ft.alignment.center
                )
            ],
            spacing=10
        ),
        margin=ft.margin.only(top=20),
        width=300
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
                                ft.Text(med["nombre"], weight=ft.FontWeight.BOLD),
                                ft.Text(f"Dosificación: {med['dosificacion']}"),
                                ft.Text(f"Intervalo: Cada {med['intervalos_dosificacion']} horas"),
                                ft.Text(f"Fecha fin: {med['fecha_fin']}")
                            ],
                            spacing=5,
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.colors.RED_600,
                            tooltip="Eliminar medicación",
                            on_click=lambda e, med_id=med["id"]: delete_medication(e, med_id)
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
            spacing=10
        ),
        padding=20,
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=10,
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
