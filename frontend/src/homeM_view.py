import flet as ft
import session_funcs as sf
import shared

def GestionarPacienteTab(page):
    codigo_field = ft.TextField(label="Codigo del Paciente", width=280)
    gestionar_button = ft.ElevatedButton(
            text="Gestionar Paciente", width=200)
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
    name_field = ft.TextField(label="Nombre", width=280)
    apellido1_field = ft.TextField(label="Apellido1", width=200)
    apellido2_field = ft.TextField(label="Apellido2", width=200)
    dni_field = ft.TextField(label="DNI", width=280)
    birth_field = ft.TextField(label="Fecha nacimiento", width=280)
    phone_field = ft.TextField(label="Número teléfono", width=280)
    password_field = ft.TextField(label="Contraseña", password=True, width=280)
    password_confirmation_field = ft.TextField(label="Confirmar Contraseña", password=True, width=280)

    register_button = ft.ElevatedButton(
        text="Registrarse",
        on_click=lambda e: sf.register_user(page, dni_field, birth_field, password_field, password_field, phone_field)
    )

    return ft.Column(
        [
            name_field,
            ft.Row(
                [
                    apellido1_field,
                    apellido2_field
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
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
    page.title = "Mi Medicación"
    
    # Top navigation bar
    profile_name = "Juan Pérez"  # This would come from actual user data
    Vis = ft.Container()
    if (page.route == "/homem"):
        Vis.content = ft.Text(value="Aqui no hay nada todavía manin")
    elif (page.route == "/homem/ges"):
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
    

# Update main.py to include this route
