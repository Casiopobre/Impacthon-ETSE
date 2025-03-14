import flet as ft
from datetime import datetime
import requests
import shared

def get_recetas(dni: str):
    return requests.get("http://"+ shared.SERVER_IP +":8080/getRecetas").json()

def otplogin(page: ft.Page, codigo_field=None):
    response = requests.post("http://"+ shared.SERVER_IP +":8080/authToken", json={
        "tokenLogin": codigo_field.value,
    }).json()
    print(response)
    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(response.get("mensaje")))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return
    elif response.get("correcto") == 1:
        # Redireccion a home
        page.client_storage.set("sessionToken", response.get("tokenLogin"))
        page.client_storage.set("id", response.get("id"))
        page.client_storage.set("tipo", "paciente")
        page.go("/homep")
        page.go("/homep")
        return
    return

def login(page: ft.Page, dni, passwd):
    """Procesa el inicio de sesión y dirige al usuario según su tipo."""
    if not dni.value or not passwd.value:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return


    # response_test = requests.post("http://"+ shared.SERVER_IP +":8080/authPWD", json={"dni": dni.value, "passwd": passwd.value})
    response = requests.post("http://"+ shared.SERVER_IP +":8080/authPWD", json={"dni": dni.value, "passwd": passwd.value}).json()
    # response = {
    #     "correcto": 1,
    #     "tokenLogin": "dummyToken123",
    #     "id": 1,
    #     "tipoUsuario": "Paciente"
    # }
    
    print("------------------------------------")
    print(response)
    print(response)
    print(response)
    print("------------------------------------")

    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(response.get("mensaje")))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return
    elif response.get("correcto") == 1:
        
        token = response.get("tokenLogin")
        user_id = response.get("id")
        tipo = response.get("tipoUsuario")
        # Save token to local storage
        page.client_storage.set("sessionToken", token)
        page.client_storage.set("id", user_id)
        page.client_storage.set("tipo", tipo)
        # Redireccion a home
        page.go("/homep")
        return 
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas o usuario no encontrado"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()

def register_user(page: ft.Page, dni_field, name_field, password_field, fecha_nac_field, num_tlf_field):
    """Procesa el registro de un nuevo paciente."""

    
    # AJUSTAR !!!!
    response = requests.post("http://"+ shared.SERVER_IP +":8080/createAct", json={
        "dni": dni_field.value,
        "passwd": password_field.value,
        "fecha": fecha_nac_field.value,
        "nombreCompleto": name_field.value,  # Replace with actual value if available
        "num_tlf": num_tlf_field.value  # Replace with actual value if available
    }).json()

    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(response.get("mensaje")))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return
    elif response.get("correcto") == 1:
        # Redireccion a home
        page.launch_url()
        page.go("/none")
        return 
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
    page.update()
    





