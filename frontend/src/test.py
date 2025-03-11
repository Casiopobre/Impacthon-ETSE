import flet as ft
from datetime import datetime

# Simulación de "base de datos" de usuarios
users_db = {
    "12345678A": {
        "dni": "12345678A",
        "edad": 30,
        "password": "1234",
        "fecha_nacimiento": "1995-01-01",
        "tipo": "Paciente",
        "nombre": "Juan Pérez"
    },
    "98765432B": {
        "dni": "98765432B",
        "edad": 40,
        "password": "abcd",
        "fecha_nacimiento": "1985-05-05",
        "tipo": "ProfesionalSalud",
        "nombre": "Dr. López"
    }
}

# Simulación de datos de recetas (tabla Receta)
recetas_db = [
    {
        "dni": "12345678A",
        "dosificacion": "2 comprimidos",
        "fecha_fin": "2025-04-30",
        "intervalos_dosificacion": 8
    },
    {
        "dni": "12345678A",
        "dosificacion": "1 jarabe",
        "fecha_fin": "2025-05-10",
        "intervalos_dosificacion": 12
    }
]

def get_recetas_by_dni(dni: str):
    """Devuelve las recetas asociadas a un paciente (según su DNI)."""
    return [rec for rec in recetas_db if rec["dni"] == dni]


def build_login_view(page: ft.Page):
    """Construye la vista de inicio de sesión y registro en pestañas."""
    # Determinamos si estamos en móvil para ajustar dimensiones
    is_mobile = page.width < 600 if page.width else False
    field_width = page.width * 0.8 if is_mobile else 300

    # Crear referencias para los campos
    login_dni_ref = ft.Ref[ft.TextField]()
    login_password_ref = ft.Ref[ft.TextField]()
    login_tipo_ref = ft.Ref[ft.Dropdown]()
    
    reg_dni_ref = ft.Ref[ft.TextField]()
    reg_edad_ref = ft.Ref[ft.TextField]()
    reg_password_ref = ft.Ref[ft.TextField]()
    reg_password_confirm_ref = ft.Ref[ft.TextField]()
    reg_fecha_nac_ref = ft.Ref[ft.TextField]()

    login_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.TextField(label="DNI", ref=login_dni_ref, width=field_width),
                ft.TextField(label="Contraseña", ref=login_password_ref, password=True, width=field_width),
                ft.Dropdown(
                    label="Tipo de Usuario",
                    ref=login_tipo_ref,
                    width=field_width,
                    options=[
                        ft.dropdown.Option("Paciente"),
                        ft.dropdown.Option("ProfesionalSalud")
                    ],
                    value="Paciente"  # valor por defecto
                ),
                ft.ElevatedButton(
                    "Iniciar Sesión", 
                    on_click=lambda e: login_user(
                        page, 
                        login_dni_ref.current, 
                        login_password_ref.current, 
                        login_tipo_ref.current
                    ), 
                    width=field_width
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    register_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.TextField(label="DNI", ref=reg_dni_ref, width=field_width),
                ft.TextField(label="Edad", ref=reg_edad_ref, width=field_width, keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Contraseña", ref=reg_password_ref, password=True, width=field_width),
                ft.TextField(label="Confirmar Contraseña", ref=reg_password_confirm_ref, password=True, width=field_width),
                ft.TextField(label="Fecha de Nacimiento", ref=reg_fecha_nac_ref, width=field_width, 
                             hint_text="YYYY-MM-DD"),
                ft.ElevatedButton(
                    "Registrarse", 
                    on_click=lambda e: register_user(
                        page, 
                        reg_dni_ref.current,
                        reg_edad_ref.current,
                        reg_password_ref.current,
                        reg_password_confirm_ref.current,
                        reg_fecha_nac_ref.current
                    ), 
                    width=field_width
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    
    # Crear las pestañas y configurar la vista
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Iniciar Sesión", content=login_tab),
            ft.Tab(text="Registrarse", content=register_tab),
        ],
        expand=True
    )
    
    page.views.clear()
    page.views.append(
        ft.View(
            "/",
            controls=[tabs],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

def login_user(page: ft.Page, dni_field, password_field, tipo_dropdown):
    """Procesa el inicio de sesión y dirige al usuario según su tipo."""
    if not dni_field.value or not password_field.value:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos"))
        page.snack_bar.open = True
        page.snack_bar.update()
        return

    dni = dni_field.value
    password = password_field.value
    tipo = tipo_dropdown.value

    if dni in users_db and users_db[dni]["password"] == password and users_db[dni]["tipo"] == tipo:
        if tipo == "Paciente":
            show_paciente_home(page, users_db[dni])
        elif tipo == "ProfesionalSalud":
            show_profesional_home(page, users_db[dni])
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas o usuario no encontrado"))
        page.snack_bar.open = True
        page.snack_bar.update()

def register_user(page: ft.Page, dni_field, edad_field, password_field, password_confirm_field, fecha_nac_field):
    """Procesa el registro de un nuevo paciente."""
    if not dni_field.value or not edad_field.value or not password_field.value or not password_confirm_field.value or not fecha_nac_field.value:
        page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"))
        page.snack_bar.open = True
        page.snack_bar.update()
        return
    
    dni = dni_field.value
    try:
        edad = int(edad_field.value)
    except ValueError:
        page.snack_bar = ft.SnackBar(ft.Text("La edad debe ser un número"))
        page.snack_bar.open = True
        page.update()
        return

    password = password_field.value
    password_confirm = password_confirm_field.value
    fecha_nac = fecha_nac_field.value

    if password != password_confirm:
        page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
        page.snack_bar.open = True
        page.update()
        return

    if dni in users_db:
        page.snack_bar = ft.SnackBar(ft.Text("El usuario ya existe"))
        page.snack_bar.open = True
        page.update()
        return

    # Se registra el usuario como Paciente.
    users_db[dni] = {
        "dni": dni,
        "edad": edad,
        "password": password,
        "fecha_nacimiento": fecha_nac,
        "tipo": "Paciente",
        "nombre": f"Paciente {dni}"  # En este ejemplo usamos el DNI como parte del nombre
    }
    page.snack_bar = ft.SnackBar(ft.Text("Registrado exitosamente, por favor inicia sesión"))
    page.snack_bar.open = True
    
    # Limpiar campos
    dni_field.value = ""
    edad_field.value = ""
    password_field.value = ""
    password_confirm_field.value = ""
    fecha_nac_field.value = ""
    
    # Cambiar la pestaña a "Iniciar Sesión"
    tabs = page.views[0].controls[0]
    tabs.selected_index = 0
    page.update()

def create_responsive_grid(controls, is_mobile):
    """Crea una cuadrícula responsiva para mostrar elementos."""
    if is_mobile:
        return ft.Column(
            controls=controls,
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
    else:
        # Si no hay suficientes controles, no dividir
        if len(controls) <= 1:
            return ft.Column(
                controls=controls,
                spacing=10,
                scroll=ft.ScrollMode.AUTO
            )
            
        mid = len(controls) // 2
        return ft.Row(
            controls=[
                ft.Column(
                    controls=controls[:mid],
                    spacing=10,
                    expand=True
                ),
                ft.Column(
                    controls=controls[mid:],
                    spacing=10,
                    expand=True
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )

def show_paciente_home(page: ft.Page, user: dict):
    """Construye la vista principal para un Paciente."""
    # Determinar si estamos en móvil
    is_mobile = page.width < 600 if page.width else False
    
    # Se consultan las recetas (medicamentos) del paciente.
    recetas = get_recetas_by_dni(user["dni"])
    
    med_cards = []
    for rec in recetas:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Dosificación: {rec['dosificacion']}", weight="bold"),
                        ft.Text(f"Fecha Fin: {rec['fecha_fin']}"),
                        ft.Text(f"Intervalo: Cada {rec['intervalos_dosificacion']} horas")
                    ],
                    spacing=10
                ),
                padding=15
            ),
            elevation=5,
            margin=10,
            width=page.width * 0.9 if is_mobile else 300
        )
        med_cards.append(card)

    # Se crea una lista simple que simula el calendario mostrando las fechas de caducidad.
    calendar_list = []
    for rec in recetas:
        calendar_list.append(
            ft.Container(
                content=ft.Text(f"Receta expira: {rec['fecha_fin']}"),
                border=ft.border.all(1, "#B3E0FF"),  # Usando color hexadecimal en vez de ft.colors
                border_radius=8,
                padding=10
            )
        )

    # Top bar con el nombre del paciente a la derecha.
    top_bar = ft.AppBar(
        leading=ft.Icon(ft.icons.MEDICATION),
        leading_width=40,
        title=ft.Text("Seguimiento de Medicación"),
        center_title=False,
        bgcolor="#2196F3",  # Azul en hexadecimal en vez de ft.colors.BLUE
        actions=[
            ft.Text(f"{user['nombre']}", size=16, color="white"),
            ft.IconButton(
                icon=ft.icons.LOGOUT,
                icon_color="white",
                on_click=lambda e: build_login_view(page)
            )
        ],
    )

    meds_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Medicamentos:", size=18, weight="bold"),
                create_responsive_grid(med_cards, is_mobile)
            ],
            spacing=10
        ),
        padding=10
    )

    calendar_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Calendario de recetas:", size=18, weight="bold"),
                ft.Column(controls=calendar_list, spacing=10)
            ],
            spacing=10
        ),
        padding=10
    )

    paciente_home = ft.Column(
        controls=[
            top_bar,
            ft.Divider(),
            meds_section,
            ft.Divider(),
            calendar_section
        ],
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        expand=True
    )

    page.views.clear()
    page.views.append(ft.View(
        "/paciente_home",
        controls=[paciente_home],
        bgcolor="white",
        padding=0
    ))
    page.update()

def show_profesional_home(page: ft.Page, user: dict):
    """Vista de ejemplo para ProfesionalSalud."""
    # Determinar si estamos en móvil
    is_mobile = page.width < 600 if page.width else False
    
    # Top bar con el nombre del profesional
    top_bar = ft.AppBar(
        leading=ft.Icon(ft.icons.HEALTH_AND_SAFETY),
        leading_width=40,
        title=ft.Text("Panel de Profesional"),
        center_title=False,
        bgcolor="#4CAF50",  # Verde en hexadecimal en vez de ft.colors.GREEN
        actions=[
            ft.Text(f"{user['nombre']}", size=16, color="white"),
            ft.IconButton(
                icon=ft.icons.LOGOUT,
                icon_color="white",
                on_click=lambda e: build_login_view(page)
            )
        ],
    )

    content = ft.Column(
        controls=[
            top_bar,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Bienvenido, {user['nombre']}", size=20, weight="bold"),
                        ft.Text("Esta sección está en desarrollo.", italic=True),
                        ft.Container(
                            content=ft.Text("Panel de administración de pacientes", size=16),
                            bgcolor="#E8F5E9",  # Verde claro en hexadecimal
                            border_radius=10,
                            padding=15,
                            margin=10
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Gestionar Pacientes",
                                    icon=ft.icons.PEOPLE,
                                    disabled=True
                                ),
                                ft.ElevatedButton(
                                    "Nuevas Recetas",
                                    icon=ft.icons.ADD_CHART,
                                    disabled=True
                                )
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                margin=20,
                expand=True
            )
        ],
        spacing=0,
        expand=True
    )
    
    page.views.clear()
    page.views.append(ft.View(
        "/profesional_home",
        controls=[content],
        bgcolor="white",
        padding=0
    ))
    page.update()

def main(page: ft.Page):
    page.title = "Seguimiento de Medicación"
    
    # Establecer tema de la aplicación
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed="#2196F3"  # Azul en hexadecimal en vez de ft.colors.BLUE
    )
    
    # Configuración para ser responsive
    def on_resize(e):
        # Esta función se llamará cuando cambie el tamaño de la ventana
        if len(page.views) > 0:
            route = page.views[-1].route
            if route == "/":
                build_login_view(page)
            elif route == "/paciente_home":
                # Como es un ejemplo, usamos un usuario fijo
                if "12345678A" in users_db:
                    show_paciente_home(page, users_db["12345678A"])
            elif route == "/profesional_home":
                if "98765432B" in users_db:
                    show_profesional_home(page, users_db["98765432B"])
    
    page.on_resize = on_resize
    
    # Iniciar con la vista de login
    build_login_view(page)

# Ejecutar la aplicación
ft.app(target=main)