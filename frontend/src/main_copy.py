import flet as ft
import cipher as cp
import requests

SERVER_IP = "143.47.54.76"

# def main(page: ft.Page):
#     page.title = "Basic Cipher/Decipher App"
#     page.window_width = 640
#     page.window_height = 480
#     page.window_resizable = False
#     page.padding = 48
#     page.margin = 48

#     def button_clicked(e):    
#         texto.value=(requests.get("http://"+ SERVER_IP +":8080/calendario").json())
#         page.update()

#     botonTest=ft.TextButton(text="Text button", on_click=button_clicked)
#     texto=ft.Text("Size 70, w900, selectable", size=70, weight=ft.FontWeight.W_900, selectable=True)


#     page.add(
#         texto,
#         botonTest
#     )


    

# ft.app(
#     target = main,
#     #view = ft.WEB_BROWSER,
# )

# A basic login component (a form) using your template style.
class LoginComponent(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(spacing=20, horizontal_alignment="center")
        self.page = page

        # Container for styling
        container = ft.Container(
            content=self,
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.BLACK12)
        )
        self.controls.append(container)
        
        # Header text
        self.controls.append(ft.Text("Login", size=32))
        
        # Email input
        self.email_field = ft.TextField(label="Email", width=300)
        self.controls.append(self.email_field)
        
        # Password input
        self.password_field = ft.TextField(label="Password", password=True, width=300)
        self.controls.append(self.password_field)
        
        # Login button
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login_clicked)
        self.controls.append(self.login_button)

    def login_clicked(self, e):
        # Placeholder: implement your authentication logic here
        print("Logging in with:", self.email_field.value)
        # For example, redirect to a dashboard route after login:
        self.page.go("/dashboard")


# Main function that sets up route handling
def main(page: ft.Page):
    page.title = "Iniciar sesión"

    # Función para manejar el cambio de ruta
    def route_change(e):
        page.views.clear()
        if page.route == "/login":
            # View del login usando el componente de Login
            login_view = ft.View(
                "/login",
                controls=[
                    # ???
                    ft.AppBar(
                        title=ft.Text("Login", size=32),
                        bgcolor=ft.Colors.DEEP_ORANGE_800,
                    ),
                    LoginComponent(page)
                ]
            )
            page.views.append(login_view)
        else:
            # Default view (for example, a Home page)
            default_view = ft.View(
                "/",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Home", size=32),
                        bgcolor=ft.Colors.DEEP_ORANGE_800,
                    ),
                    ft.Text("Welcome to the Home Page", size=32)
                ]
            )
            page.views.append(default_view)
        page.update()

    # Set the route change handler.
    page.on_route_change = route_change

    if page.route == "/":
        page.go("/login")
    else:
        page.go(page.route)

ft.app(target=main)
