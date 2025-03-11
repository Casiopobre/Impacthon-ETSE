import flet as ft
from datetime import datetime
import requests

def get_recetas(dni: str):
        return requests.get("http://"+ SERVER_IP +":8080/getRecetas").json()


def session_view(page: ft.Page):
    is_mobile = page.width < 600 if page.width else False
    field_width = page.width * 0.8 if is_mobile else 300

    page.title = "Iniciar sesión"

    # Crear referencias para los campos
    login_dni_ref = ft.Ref[ft.TextField]()
    login_password_ref = ft.Ref[ft.TextField]()
    login_tipo_ref = ft.Ref[ft.Dropdown]()
    
    reg_dni_ref = ft.Ref[ft.TextField]()
    reg_edad_ref = ft.Ref[ft.TextField]()
    reg_password_ref = ft.Ref[ft.TextField]()
    reg_password_confirm_ref = ft.Ref[ft.TextField]()
    reg_fecha_nac_ref = ft.Ref[ft.TextField]()  

    login_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.TextField(label="DNI", ref=login_dni_ref, width=field_width),
                ft.TextField(label="Contraseña", ref=login_password_ref, password=True, width=field_width),
                ft.Dropdown(
                    label="Tipo de Usuario",
                    ref=login_tipo_ref,
                    width=field_width,
                    options=[
                        ft.dropdown.Option("Paciente"),
                        ft.dropdown.Option("ProfesionalSalud")
                    ],
                    value="Paciente"  # valor por defecto
                ),
                ft.ElevatedButton(
                    "Iniciar Sesión", 
                    on_click=lambda e: login_user(
                        page, 
                        login_dni_ref.current, 
                        login_password_ref.current, 
                        login_tipo_ref.current
                    ), 
                    width=field_width
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    register_tab = ft.Container(
        content=ft.Column(
            controls=[
                ft.TextField(label="DNI", ref=reg_dni_ref, width=field_width),
                ft.TextField(label="Edad", ref=reg_edad_ref, width=field_width, keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Contraseña", ref=reg_password_ref, password=True, width=field_width),
                ft.TextField(label="Confirmar Contraseña", ref=reg_password_confirm_ref, password=True, width=field_width),
                ft.TextField(label="Fecha de Nacimiento", ref=reg_fecha_nac_ref, width=field_width, 
                             hint_text="YYYY-MM-DD"),
                ft.ElevatedButton(
                    "Registrarse", 
                    on_click=lambda e: register_user(
                        page, 
                        reg_dni_ref.current,
                        reg_edad_ref.current,
                        reg_password_ref.current,
                        reg_password_confirm_ref.current,
                        reg_fecha_nac_ref.current
                    ), 
                    width=field_width
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True
    )

def token_login(page: ft.Page, codigo_field=None):
    
    
    return

def login(page: ft.Page, dni_field, password_field):
    
    """Procesa el inicio de sesión y dirige al usuario según su tipo."""
    if not dni_field.value or not password_field.value:
        page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos"))
        page.snack_bar.open = True
        page.snack_bar.update()
        return

    dni = dni_field.value
    password = password_field.value
    response = requests.post("http://"+ SERVER_IP +":8080/authPWD", data={"dni": dni, "passwd": password}).json()
    
    if response.get("correcto") == 0:
        # error
        page.snack_bar = ft.SnackBar(ft.Text(
            response.get("mensaje")
        ))
        page.snack_bar.open = True
        page.snack_bar.update()
        return
    elif response.get("correcto") == 1:
        token = response.get("tokenLogin")
        # Save token to local storage
        page.client_storage.set("token", token)
        # Redireccion a home
        page.go("/phome")
        return 
        # users_db[dni] = {
        #     "dni": dni,
        #     "token": token,
        #     "tipo": "Paciente",
        #     "nombre": f"Paciente {dni}"  # En este ejemplo usamos el DNI como parte del nombre
        # }
        show_paciente_home(page, users_db[dni])
        
        
        
        return

    if usar_token and tipo == "ProfesionalSalud":
        req_session = requests.post("http://"+ SERVER_IP +":8080/login", data={"dni": dni, "password": password}).json()
        if "error" in token:
            page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas o usuario no encontrado"))
            page.snack_bar.open = True
            page.snack_bar.update()
            return
        users_db[dni] = {
            "dni": dni,
            "token": token,
            "tipo": "ProfesionalSalud",
            "nombre": f"Profesional de Salud {dni}"  # En este ejemplo usamos el DNI como parte del nombre
        }
        show_profesional_home(page, users_db[dni])
        return
    elif not usar_token and tipo == "Paciente":
        

    if not usar_token and tipo == "ProfesionalSalud":
        req_session

    if not usar_token and tipo == "ProfesionalSalud":

    if dni in users_db and users_db[dni]["password"] == password and users_db[dni]["tipo"] == tipo:
        if tipo == "Paciente":
            show_paciente_home(page, users_db[dni])
        elif tipo == "ProfesionalSalud":
            show_profesional_home(page, users_db[dni])
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas o usuario no encontrado"))
        page.snack_bar.open = True
        page.snack_bar.update()




def register_user(page: ft.Page, dni_field, edad_field, password_field, password_confirm_field, fecha_nac_field):
    """Procesa el registro de un nuevo paciente."""
    if not dni_field.value or not edad_field.value or not password_field.value or not password_confirm_field.value or not fecha_nac_field.value:
        page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"))
        page.snack_bar.open = True
        page.snack_bar.update()
        return
    
    dni = dni_field.value
    try:
        edad = int(edad_field.value)
    except ValueError:
        page.snack_bar = ft.SnackBar(ft.Text("La edad debe ser un número"))
        page.snack_bar.open = True
        page.update()
        return

    password = password_field.value
    password_confirm = password_confirm_field.value
    fecha_nac = fecha_nac_field.value

    if password != password_confirm:
        page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
        page.snack_bar.open = True
        page.update()
        return



    if dni in users_db:
        page.snack_bar = ft.SnackBar(ft.Text("El usuario ya existe"))
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
