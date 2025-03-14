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

    page.pub_static_dir = "frontend/src/assets" 
    
    # Define fixed routes
    routes = [
        "/session/login",
        "/session/otplogin",
        "/session/register",
        "/homep",
        "/homem",
        "/homem/ges",
        "/homem/an",
        "/homep/sintomas"
    ]
    page.launch_url = "/none"
    page.go("/none")
    # Helper function to check if a route is a valid temporary patient route
    #asda
    
    def is_valid_temp_patient_route(route):
        if route.startswith("/homem/ges"):
            # Check if route exists in temp routes dictionary
            if route in homeM_funcs.temp_patient_routes:
                # Check if route hasn't expired
                expiration = homeM_funcs.temp_patient_routes[route]["expiration"]
                if datetime.datetime.now() < expiration:
                    return True
                else:
                    # Route has expired, remove it
                    del homeM_funcs.temp_patient_routes[route]
            else:
                return False
        else:
            return False
    

    # Función para construir la vista de síntomas
    

        
    def type_checker(page):
        return page.client_storage.get("tipo")

    def to_home_redirect(page):
        if type_checker(page) == "paciente":
            page.go("/homep")
        elif type_checker(page) == "medico":
            page.go("/homem")
            
    # Función para manejar el cambio de ruta
    def reroute(e):
        page.views.clear()
        page.adaptive = True
        page.title = "CuidaMed"
        # Check for temporary patient routes first
        
    
        # Check for session token        
        if page.client_storage.get("sessionToken"):
            print("Hay token")
            if e.route in routes:
                if e.route.startswith("/session"):
                    # redirigimos al home correspondiente
                    to_home_redirect(page)
                    
                elif e.route.startswith("/homep"):
                    if type_checker(page) == "paciente":
                        if e.route == "/homep/sintomas":
                            page.views.append(homeP_view.build_symptom_menu_view(page))
                        else:
                        # View del home del pacientee
                            page.views.append(homeP_view.build_homeP_view(page))
                    
                    else:
                        to_home_redirect(page)
                        
                
                elif e.route.startswith("/homem"):
                    if type_checker(page) == "medico":
                        # View del home del médico
                        page.views.append(homeM_view.build_homeM_view(page))
                    else:
                        to_home_redirect(page)
            elif is_valid_temp_patient_route(e.route):
                # Get patient ID from the temporary route data
                page.views.append(homeM_view.GestionarPacienteObtenido(page, homeM_funcs.temp_patient_routes[e.route]["patient_id"]))
            
            else:
                to_home_redirect(page)
        else:
            print("No session token found")
            if e.route not in routes:
                page.go("/session/login")
            elif e.route.startswith("/session"):
                page.views.append(session_view.build_view(page))
            else:
                page.go("/session/login")     

        page.update()

    # Set the route change handler
    page.on_route_change = reroute
    
    # Initial route
# aasdasd
ft.app(target=main)


        