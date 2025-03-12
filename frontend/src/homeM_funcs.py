import flet as ft
import requests
import time
import shared
from datetime import datetime, timedelta

# Store temporary routes with expiration times
temp_patient_routes = {}

def gestionar_paciente(page: ft.Page, codigo_paciente=None):
    """
    Processes token authentication for managing patient data
    Creates a temporary route that expires after 15 minutes
    """
    if not codigo_paciente:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, introduce un código de paciente"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return

    # # Make request to backend
    # response = requests.post("http://" + shared.SERVER_IP + ":8080/authToken", 
    #                        json={"tokenLogin": codigo_paciente}).json()
    # Dummy response for testing
    response = {
        "correcto": 1,
        "id": "12345",
        "mensaje": "Autenticación exitosa"
    }
    if response.get("correcto") == 1:

        # Get patient ID
        patient_id = response.get("id")
        
        # Create temporary route with expiration time
        temp_route = f"/homem/ges/{patient_id}"
        expiration_time = datetime.now() + timedelta(minutes=1)
        
        # Store the route with its expiration time
        temp_patient_routes[temp_route] = {
            "expiration": expiration_time,
            "patient_id": patient_id
        }
       
       
        print("\n\n\n  - -- - - Autenticación exitosa \n\n\n")
        print(temp_route)
        print(temp_patient_routes)
        print("\n\n\n  - -- - - Autenticación exitosa \n\n\n")
         
        # Navigate to the temporary route
        page.snack_bar = ft.SnackBar(ft.Text(f"Acceso concedido a datos del paciente. Expira en 15 minutos."))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        
        # Navigate to patient data page
        page.go(temp_route)
        
    else:
        # Show error message
        error_msg = response.get("mensaje", "Error de autenticación")
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error_msg}"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()