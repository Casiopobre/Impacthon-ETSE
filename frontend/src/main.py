import flet as ft
import cipher as cp
import session_view as session_view
import shared


# -----------------------------
# Main Session View with Tabs
# -----------------------------


def main(page: ft.Page):
    page.adaptive = True
    page.title = "Iniciar sesión"

    # Función para manejar el cambio de ruta
    def reroute(e):
        page.views.clear()

        if page.route.startswith("/session"):
            print("\n\n\n\n\n\n\n Rerouting to SESSION view \n\n\n\n\n\n\n")        
            page.views.append(session_view.build_view(page))


        elif page.route.startswith("/home"):
            print("\n\n\n\n\n\n\n Rerouting to HOME view \n\n\n\n\n\n\n")        
            page.views.append(shared.PHomeView(page))
        # elif page.route == "/mhome":
        #     # View del home de profesional sanitario
        # elif page.route == "/register": 
        #     # View del registro de usuario

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
    page.on_route_change = reroute

    if page.route == "/" and page.client_storage.get("sessionToken") == None:
        page.go("/session/login")
    else:
        page.go(page.route)

ft.app(target=main)
