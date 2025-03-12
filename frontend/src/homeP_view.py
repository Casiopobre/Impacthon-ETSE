import flet as ft
import session_funcs as sf
import shared
from calendario import Calendario

def build_homeP_view(page: ft.Page):
    """
    Construye la vista principal del paciente con la lista de medicamentos y espacio para el calendario.
    """
    page.title = "Mi Medicación"
    
    # Function to handle feeling button click
    def open_feeling_dialog(e):
        feeling_dialog = ft.AlertDialog(
            title=ft.Text("¿Cómo te sientes?"),
            content=ft.Column([
                ft.TextField(label="blablabla")
            ], tight=True, spacing=20),
            actions=[
            ft.ElevatedButton(
                "Cancelar",
                on_click=lambda e: setattr(feeling_dialog, "open", False)
            ),
            ft.ElevatedButton(
                "Enviar",
                on_click=lambda e: setattr(feeling_dialog, "open", False)
            )
            ]
        )
        page.dialog = feeling_dialog
        feeling_dialog.open = True
        page.update()
        return 
    # Top navigation bar
    profile_name = "Juan Pérez"  # This would come from actual user data
    
    nav_bar = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.DOUBLE_ARROW,
                icon_color=ft.colors.WHITE,
                tooltip="Cambiar perfil",
                on_click=lambda e: print("Switch profile clicked")
            ),
            # ft.Spacer(),
            ft.Text(profile_name, color=ft.colors.WHITE, size=16),
            ft.Container(
                content=ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30, color=ft.colors.WHITE),
                margin=ft.margin.only(left=10)
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Feeling button
    feeling_button = ft.ElevatedButton(
        "¿Cómo te sientes?",
        icon=ft.icons.MOOD,
        on_click=open_feeling_dialog,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.all(15),
        )
    )

    # Medication list - this would typically be populated from a database
    def get_medication_data():
        # This would be replaced with an actual API call like sf.get_recetas(user_dni)
        # For now, returning sample data
        return [
            {"name": "Paracetamol", "dose": 500, "interval": 8, "image": "paracetamol.png"},
            {"name": "Ibuprofeno", "dose": 400, "interval": 6, "image": "ibuprofeno.png"},
            {"name": "Omeprazol", "dose": 20, "interval": 24, "image": "omeprazol.png"},
            {"name": "Amoxicilina", "dose": 750, "interval": 12, "image": "amoxicilina.png"},
        ]

    # Function to create a medication card
    def create_medication_card(medication):
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        # Left side - medication image
                        ft.Container(
                            content=ft.Icon(
                                ft.icons.MEDICATION,
                                size=40,
                                color=ft.colors.BLUE_400,
                            ),
                            width=60,
                            height=60,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.BLUE_50,
                            border_radius=ft.border_radius.all(10),
                        ),
                        
                        # Right side - medication details
                        ft.Column(
                            [
                                ft.Text(medication["name"], weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Dosis: {medication['dose']} mg", size=14),
                                ft.Text(f"Intervalo: Cada {medication['interval']} horas", size=14),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
            ),
            margin=ft.margin.only(bottom=10),
            elevation=2,
        )

    # Create medication list
    medication_list = ft.ListView(
        spacing=10,
        padding=20,
        expand=True,
    )
    
    # Populate medication list
    medications = get_medication_data()
    for medication in medications:
        medication_list.controls.append(create_medication_card(medication))

    # Container for the calendar 
    calendario = Calendario()

    calendar_container = ft.Container(
        content=calendario.get_calendar_view(),
        padding=20,
        expand=False
    )

    # Main content layout - responsive
    def get_content_layout():
        # Check if we're on mobile
        if page.width < 600:
            # Mobile layout: Calendar under medication list
            return ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Medicamentos de hoy", size=20, weight=ft.FontWeight.BOLD),
                                medication_list,
                            ],
                        ),
                        expand=True,
                    ),
                    calendar_container,
                ],
                expand=True,
            )
        else:
            # Desktop/web layout: Calendar to the right of medication list
            return ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Medicamentos de hoy", size=20, weight=ft.FontWeight.BOLD),
                                medication_list,
                            ],
                        ),
                        expand=True,
                    ),
                    calendar_container,
                ],
                expand=True,
            )

    # Update layout when window size changes
    page.on_resize = lambda _: page.update()

    # Main view
    return ft.View(
        route="/home",
        controls=[
            # AppBar with navigation
            ft.AppBar(
                title=ft.Text("Mi Medicación"),
                bgcolor=ft.colors.DEEP_ORANGE_800,
                actions=[nav_bar],
            ),
            # Feeling button in a container
            ft.Container(
                content=feeling_button,
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20, bottom=10),
            ),
            # Main content (responsive)
            get_content_layout(),
        ],
    )

# Update main.py to include this route