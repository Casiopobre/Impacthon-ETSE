import flet as ft
import session_funcs as sf
import shared

def NormalLogin(page):
        dni_field = ft.TextField(label="DNI", width=280)
        password_field = ft.TextField(label="Contraseña", password=True, width=280)
        
        otp_button = ft.ElevatedButton(
            text="Inicio de sesión con código de un solo uso",
            on_click=lambda _: page.go("/session/otplogin")
        )

        login_button = ft.ElevatedButton(
            text="Iniciar sesión",
            on_click=lambda _: sf.login(page, dni_field, password_field)
        )
<<<<<<< HEAD
        register_button = ft.ElevatedButton(
             text="Registrarse",
             on_click=lambda e: page.go("/session/register")
        )
        print("\n\n\n\n\n Hola \n\n\n\n\n")
=======

        register_button = ft.ElevatedButton(
            text="Registrarse",
            on_click=lambda _: page.go("/session/register")
        )

        print("\n\n estás en login \n\n")
>>>>>>> ce9c9db4540d8f87cd0baaba7c931685d10d47d3

        return ft.Column(
            [
                ft.Row([
<<<<<<< HEAD
                        register_button
                    ],
                    alignment=ft.MainAxisAlignment.END),
                dni_field,
                password_field,
                login_button,
                otp_button
=======
                    login_button,
                    register_button
                ]),
                ft.Row([
                    dni_field,
                    password_field,

                ]),
                ft.Row([                    
                    login_button,
                    otp_button
                ]),
>>>>>>> ce9c9db4540d8f87cd0baaba7c931685d10d47d3
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )


def OptLogin(page):
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


def Register(page):
        name_field = ft.TextField(label="Nombre completo", width=280)
        dni_field = ft.TextField(label="DNI", width=280)
        birth_field = ft.TextField(label="Fecha nacimiento", width=280)
        phone_field = ft.TextField(label="Número teléfono", width=280)
        password_field = ft.TextField(label="Contraseña", password=True, width=280)
        confirm_password_field = ft.TextField(label="Contraseña", password=True, width=280)

        register_button = ft.ElevatedButton(
            text="Registrarse",
            on_click=lambda e: sf.register_user(page, dni_field, name_field, password_field, birth_field)
        )

        return ft.Column(
            [
                name_field,
                dni_field,
                birth_field,
                phone_field,
                password_field,
                confirm_password_field,
                register_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )


def build_view(page: ft.Page):
    """
    Esta vista incluye las 3 pestañas: inicio de sesión normal, inicio de sesión con OTP, registro.
    La pestaña activa depende de la ruta actual.
    """
    # Decide la pestaña que debe estar activa basado en la ruta
    # rutas posibles = '/session/login', '/session/otplogin', '/session/register'
    # mi puta madre que hay que poner el indice a mano estamos tontos

    # --#-- !!! --#--
    # REVISEN ESTO A LA MAÑANA Q NO SE QUE HAGO  
    #   - Estamos cooked
    # --#-- !!! --#--
    selected_index = 0
        
    components = []
    route_returned="/"
    if page.route == "/session/login":
    # Wrap tabs in a nice container for styling
        components = NormalLogin(page)
        route_returned="/session/login"
    elif page.route == "/session/otplogin":
        components = OptLogin(page)
        route_returned="/session/otplogin"
    elif page.route == "/session/register":
        components = Register(page)
        route_returned="/session/register"
        
    content_container = ft.Container(
        content=components,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.BLACK12),
    )
    


    # Create the top-level view
    return ft.View(
        route=route_returned,
        controls=[
            # Optionally an AppBar:
            ft.AppBar(
                bgcolor=shared.SERGAS_1_HEX,
            ),
            content_container
        ]
    )

