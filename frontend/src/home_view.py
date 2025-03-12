import flet as ft
import session_funcs as sf

def NormalLoginTab(page):
        dni_field = ft.TextField(label="DNI", width=280)
        password_field = ft.TextField(label="Contraseña", password=True, width=280)
        otp_button = ft.ElevatedButton(
            text="Inicio de sesión con código de un solo uso",
            on_click=lambda e: page.go("/session/otplogin")
        )

        login_button = ft.ElevatedButton(
            text="Iniciar sesión",
            on_click=lambda e: sf.login(page, dni_field, password_field)
        )

        print("\n\n\n\n\n Hola \n\n\n\n\n")

        return ft.Column(
            [
                dni_field,
                password_field,
                login_button,
                otp_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )


def OtpLoginTab(page):
        dni_field = ft.TextField(label="DNI", width=280)
        otp_field = ft.TextField(label="Código de un solo uso", width=280)

        login_button = ft.ElevatedButton(
            text="Iniciar sesión con OTP",
            on_click=lambda e : sf.otplogin(page, dni_field, otp_field)
        )

        return ft.Column(
            [
                dni_field,
                otp_field,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )


def RegisterTab(page):
        name_field = ft.TextField(label="Nombre y apellidos", width=280)
        dni_field = ft.TextField(label="DNI", width=280)
        birth_field = ft.TextField(label="Fecha nacimiento", width=280)
        phone_field = ft.TextField(label="Número teléfono", width=280)
        password_field = ft.TextField(label="Contraseña", password=True, width=280)

        register_button = ft.ElevatedButton(
            text="Registrarse",
            on_click=lambda e: sf.register_user(page, dni_field, birth_field, password_field, password_field, phone_field)
        )

        return ft.Column(
            [
                name_field,
                dni_field,
                birth_field,
                phone_field,
                password_field,
                register_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )


def build_view(page: ft.Page):
    """
    Esta vista incluye las pestañas de home de paciente y profesional sanitario.
    La pestaña activa depende de la ruta actual.
    """
    # Decide la pestaña que debe estar activa basado en la ruta
    # rutas posibles = '/session/login', '/session/otplogin', '/session/register'
    # mi puta madre que hay que poner el indice a mano estamos tontos

    # --#-- !!! --#--
        #  NECESITO CAFEINA NECESITO CAFEINA
    # --#-- !!! --#--

    selected_index = 0
    if page.route == "/home/p":
        selected_index = 1
    elif page.route == "/home/m":
        selected_index = 2
    # Show a snackbar when the route changes
    page.snack_bar = ft.SnackBar(
        content=ft.Text(f"Switched to tab: {selected_index + 1}"),
        action="Dismiss"
    )
    page.controls.append(page.snack_bar)
    page.snack_bar.open = True

    tabs = ft.Tabs(
        selected_index=selected_index,
        on_change=lambda e: session_tab_change(e, page),
        tabs=[
            ft.Tab(
                text="Iniciar sesión",
                content=ft.Container(
                    content=NormalLoginTab(page)
                ),
            ),
            ft.Tab(
                text="Inicio de sesión con código de un solo uso",
                content=ft.Container(
                    content=OtpLoginTab(page)
                ),            ),
            ft.Tab(
                text="Registrarme",
                content=ft.Container(
                    content=RegisterTab(page)
                ),            ),
        ]
    )

    # Wrap tabs in a nice container for styling
    content_container = ft.Container(
        content=tabs,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.colors.WHITE,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.BLACK12),
    )

    # Create the top-level view
    return ft.View(
        route=page.route,
        controls=[
            # Optionally an AppBar:
            ft.AppBar(
                title=ft.Text("Gestión de Sesión", size=32),
                bgcolor=ft.colors.DEEP_ORANGE_800,
            ),
            content_container
        ]
    )

def session_tab_change(e: ft.ControlEvent, page: ft.Page):
    """When user manually switches tabs from the UI, you can optionally sync the route here."""
    if e.control.selected_index == 0:
        page.go("/session/login")
    elif e.control.selected_index == 1:
        page.go("/session/otplogin")
    elif e.control.selected_index == 2:
        page.go("/session/register")

