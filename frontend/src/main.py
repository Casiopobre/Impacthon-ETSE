import flet as ft
import cipher as cp
import datetime
import requests
from calendario import Calendario
import session_view
import shared
import homeP_view
import homeM_view
import homeM_funcs  # Import to access temp_patient_routes

def main(page: ft.Page):
    page.adaptive = True
    page.title = "Iniciar sesión"
    
    # Define fixed routes
    routes = [
        "/session/login",
        "/session/otplogin",
        "/session/register",
        "/homep",
        "/homem",
        "/homem/ges",
        "/homem/an",
        "/sintomas",
    ]
    
    session_token = page.client_storage.get("sessionToken")
    
    # Helper function to check if a route is a valid temporary patient route
    def is_valid_temp_patient_route(route):
        if route.startswith("/homem/ges/"):
            # Check if route exists in temp routes dictionary
            if route in homeM_funcs.temp_patient_routes:
                # Check if route hasn't expired
                expiration = homeM_funcs.temp_patient_routes[route]["expiration"]
                if datetime.datetime.now() < expiration:
                    return True
                else:
                    # Route has expired, remove it
                    del homeM_funcs.temp_patient_routes[route]
        return False
    

    # Función para construir la vista de síntomas
    def build_sintomas_view():
        def on_sintoma_selected(e):
            print(f"{e.control.text} seleccionado")
            page.go("/homep")

        return ft.View(
            route="/sintomas",
            controls=[
                ft.AppBar(
                    title=ft.Text("Síntomas"),
                    bgcolor=ft.colors.DEEP_ORANGE_800,
                ),
                ft.Text("Selecciona los síntomas que tienes hoy", size=20, weight=ft.FontWeight.BOLD),
                ft.GridView(
                    controls=[
                        ft.ElevatedButton("Dolor de cabeza", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Fiebre", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Tos", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Cansancio", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Dolor muscular", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Mareos", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Náuseas", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Vómito", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Diarrea", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Estreñimiento", on_click=on_sintoma_selected),
                        ft.ElevatedButton("Congestión nasal", on_click=on_sintoma_selected),
                    ],
                    max_extent=200,
                    spacing=10,
                    run_spacing=10,
                )
            ],
        )

        
    # Función para manejar el cambio de ruta
    def reroute(e):
        page.views.clear()
        
        # Check for temporary patient routes first
        if is_valid_temp_patient_route(e.route):
            # Get patient ID from the temporary route data
            page.views.append(homeM_view.GestionarPacienteObtenido(page, homeM_funcs.temp_patient_routes[e.route]["patient_id"]))

            
        elif e.route in routes:
            if e.route.startswith("/session"):
                print("\n\n\n\n\n\n\n Rerouting to session view \n\n\n\n\n\n\n")        
                page.views.append(session_view.build_view(page))
            elif e.route == "/homep":
                # View del home del paciente
                page.views.append(homeP_view.build_homeP_view(page))
            elif e.route == "/sintomas":
                page.views.append(build_sintomas_view())
            elif e.route.startswith("/homem"):
                # View del home del médico
                page.views.append(homeM_view.build_homeM_view(page))
            else:
                # Default view
                # default_view = ft.View(
                #     "/",
                #     controls=[
                #         ft.AppBar(
                #             title=ft.Text("Home", size=32), 
                #             bgcolor=ft.colors.DEEP_ORANGE_800,
                #         ),
                #         ft.Text("Welcome to the Home Page", size=32)
                #     ]
                # )
                # page.views.append(default_view)
                # !HAY QUE CAMBIAR ESTO !!!!!!!!!!!!!!!!!
                page.go("/session/login")
        else:
            if not session_token:
                page.go("/session/login")     
            elif e.route not in routes and session_token:
                to_home_redirect(session_token, page)
            else:
                page.go("/error")  

        page.update()

    # Set the route change handler.
    page.on_route_change = reroute
    
    # Initial route
    page.go("/session/login")

ft.app(target=main)

def to_home_redirect(token, page):
    # Simplified for example
    user_type = "paciente"
    if user_type == 'paciente':
        page.go("/homep")
    elif user_type == 'profesional':
        page.go("/homem")
    else:
        page.go("/error")