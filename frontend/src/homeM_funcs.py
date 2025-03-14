import flet as ft
import requests
import time
import shared
from datetime import datetime, timedelta
import random
import string

# Store temporary routes with expiration times
temp_patient_routes = {}
temp_patient_data = {}

def format_date(iso_date_string):
    """
    Format an ISO date string to a more readable format
    
    Args:
        iso_date_string: ISO format date string
        
    Returns:
        A formatted date string like "02/02/2025"
    """
    if not iso_date_string:
        return "N/A"
    try:
        date_obj = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return iso_date_string


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

    codigo_paciente
    
    get_id = requests.post("http://" + shared.SERVER_IP + ":8080/authToken",json={"tokenLogin": codigo_paciente}).json()
    
    if get_id.get("correcto") == 1 and get_id.get("id") is not None:     

        response = requests.post("http://" + shared.SERVER_IP + ":8080/getDatosUsuario", 
                            json={"tokenLogin": page.client_storage.get("sessionToken"), "id":page.client_storage.get("id"), "idPaciente": get_id.get("id") }).json()
        print("---------------")
        print("---------------")
        print("---------------")
        print(response)
        print("---------------")
        print("---------------")
        print("---------------")


        if response.get("correcto") == 1:

            # Get patient ID
            patient_id = get_id.get("id")
            
            # Create temporary route with expiration time
            temp_route = f"/homem/ges/{patient_id}"
            expiration_time = datetime.now() + timedelta(minutes=1)

            # Store the route with its expiration time
            temp_patient_routes[temp_route] = {
                "expiration": expiration_time,
                "patient_id": patient_id
            }
            temp_patient_data[patient_id] = response
            page.client_storage.set("idPaciente", patient_id)
        
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
        return None
        
            
            
def get_paciente_recetas(page: ft.Page, id_paciente):
    # Get user data from client storage
    
    # Make request to server
    try:
        response = requests.post(
            f"http://{shared.SERVER_IP}:8080/getRecetas",
            json={"tokenLogin": page.client_storage.get("sessionToken"), "idPaciente":id_paciente, "id": page.client_storage.get("id")}
        ).json()
        print("....................")
        print("....................")
        print(id_paciente)
        print(response)
        print("....................")
        print("....................")
        
        if response.get("correcto") == 1 and "recetas" in response:
            # Transform the data to match the expected format
            medications = []
            for receta in response["recetas"]:
                medications.append({
                    "name": receta["nombre"],
                    "dose": receta["dosificacion"],
                    "interval": receta["intervalosDosificacion"],
                    "start_date": receta["fechaEmision"],
                    "end_date": receta["fechaFin"]
                })
            return medications
        else:
            print(f"Error fetching medications: {response.get('mensaje', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Exception fetching medications: {str(e)}")
        return []

def register_user(page: ft.Page, dni_field, name_field, fecha_nac_field, num_tlf_field):
    """Procesa el registro de un nuevo paciente."""
    
    # Generate random 3 letter password
    password = ''.join(random.choices(string.ascii_letters, k=3))
    # AJUSTAR !!!!
    response = requests.post("http://"+ shared.SERVER_IP +":8080/createActMedico", json={
        "id": page.client_storage.get("id"),
        "tokenLogin": page.client_storage.get("sessionToken"),
        "dni": dni_field.value,
        "passwd": password,
        "fecha": fecha_nac_field.value,
        "nombreCompleto": name_field.value,  
        "num_tlf": num_tlf_field.value  
    }).json()

    print(response)
    print("---------------")
    print("---------------")
    print(dni_field.value)
    print(password)
    print(fecha_nac_field.value)
    print(name_field.value)
    print(num_tlf_field.value)
    print("---------------")
    print("---------------")

    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(response.get("mensaje")))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return [False, None]
    elif response.get("correcto") == 1:
        # Return success
        return [True, password, response.get("token")]
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return [False, None]
    

def calculate_age(birthdate_str):
    """
    Calculate age from MySQL date string (YYYY-MM-DD)
    Returns floor of age in years
    """
    try:
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
        today = datetime.now()
        age = (today - birthdate).days / 365.25
        return int(age)
    except:
        return 0