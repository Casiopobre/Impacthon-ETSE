import flet as ft
from datetime import datetime
import requests
import shared

def get_recetas(dni: str):
    return requests.get("http://"+ shared.SERVER_IP +":8080/getRecetas").json()

def otplogin(page: ft.Page, codigo_field=None):
    return

def login(page: ft.Page, dni, passwd):
    """Procesa el inicio de sesión y dirige al usuario según su tipo."""
    if not dni.value or not passwd.value:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return

    # --- !!!! ---- DATOS DE PRUEBA BORRAR LUEGO ---- !!!! ----
    # --- !!!! ---- DATOS DE PRUEBA BORRAR LUEGO ---- !!!! ----
    # --- !!!! ---- DATOS DE PRUEBA BORRAR LUEGO ---- !!!! ----
        dummy_data = {
        "users": [
            {
                "name": "Juan",
                "dni": "12345678A",
                "birth_date": "1990-01-01",
                "phone": "+34123456789",
                "password": "password123",
                "otp": "123456",
                "tipo": "paciente"
            },
            {
                "name": "Maripuri",
                "dni": "87654321B",
                "birth_date": "1985-05-15",
                "phone": "+34987654321",
                "password": "password456",
                "otp": "654321",
                "tipo": "medico"
            }
        ]
    }

    user = next((user for user in dummy_data["users"] if user["dni"] == dni.value and user["password"] == passwd.value), None)
    if user:
        page.snack_bar = ft.SnackBar(ft.Text("Inicio de sesión exitoso"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return

    # --- !!!! ---- FIN DATOS DE PRUEBA BORRAR LUEGO ---- !!!! ----
    # --- !!!! ---- FIN DATOS DE PRUEBA BORRAR LUEGO ---- !!!! ----
    # --- !!!! ---- FIN DATOS DE PRUEBA BORRAR LUEGO ---- !!!! ----


    response = requests.post("http://"+ shared.SERVER_IP +":8080/authPWD", data={"dni": dni.value, "passwd": passwd.value}).json()
    
    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(response.get("mensaje")))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return
    elif response.get("correcto") == 1:
        token = response.get("tokenLogin")
        # Save token to local storage
        page.client_storage.set("sessionToken", token)
        # Redireccion a home
        page.go("/phome")
        return 
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas o usuario no encontrado"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()

def register_user(page: ft.Page, dni_field, name_field, password_field, fecha_nac_field):
    """Procesa el registro de un nuevo paciente."""
    if not dni_field.value or not name_field.value or not password_field.value or not fecha_nac_field.value:
        page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return
    
    # AJUSTAR !!!!
    response = requests.post("http://"+ shared.SERVER_IP +":8080/createAct", data={
        "dni": dni_field.value,
        "passwd": password_field.value,
        "nombre": name_field.value,  # Replace with actual value if available
        "num_tlf": "123456789"  # Replace with actual value if available
    }).json()

    dni = dni_field.value

    

    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(response.get("mensaje")))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return
    elif response.get("correcto") == 1:
        token = response.get("tokenLogin")
        # Save token to local storage
        page.client_storage.set("sessionToken", token)
        # Redireccion a home
        page.go("/phome")
        return 
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas o usuario no encontrado"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()

    password = password_field.value
    password_confirm = password_confirm_field.value
    fecha_nac = fecha_nac_field.value

    if password != password_confirm:
        page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return

    if dni in users_db:
        page.snack_bar = ft.SnackBar(ft.Text("El usuario ya existe"))
        page.controls.append(page.snack_bar)
        page.snack_bar.open = True
        page.update()
        return

    # Se registra el usuario como Paciente.
    users_db[dni] = {
        "dni": dni,
        "edad": edad,
        "password": password,
        "fecha_nacimiento": fecha_nac,
        "tipo": "Paciente",
        "nombre": f"Paciente {dni}"  # En este ejemplo usamos el DNI como parte del nombre
    }
    page.snack_bar = ft.SnackBar(ft.Text("Registrado exitosamente, por favor inicia sesión"))
    page.controls.append(page.snack_bar)
    page.snack_bar.open = True
    
    # Limpiar campos
    dni_field.value = ""
    edad_field.value = ""
    password_field.value = ""
    password_confirm_field.value = ""
    fecha_nac_field.value = ""
    
    # Cambiar la pestaña a "Iniciar Sesión"
    tabs = page.views[0].controls[0]
    tabs.selected_index = 0
    page.update()





