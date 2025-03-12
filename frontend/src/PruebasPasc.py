import flet as ft

class TrelloApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.edit_name = ft.TextField(expand=1)
        
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.GRID_GOLDENRATIO_ROUNDED),
            leading_width=100,
            title=ft.Text("Placeholder", size=32, text_align=ft.TextAlign.CENTER),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.DEEP_ORANGE_800,
            actions=[],
        )
        
        self.page.appbar = self.appbar
        self.update_appbar("Login", self.login_clicked)
        self.page.update()
        
    def login_clicked(self, e):
        print("Debería iniciar sesión")
        self.update_appbar("Cerrar Sesión", self.cerrar_clicked)
        
    def cerrar_clicked(self, e):
        print("Debería cerrar sesión")
        self.update_appbar("Login", self.login_clicked)
        
    def update_appbar(self, text, callback):
        popup_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text=text, on_click=callback),
                ft.PopupMenuItem(),  # divisor
                ft.PopupMenuItem(text="Settings")
            ]
        )
        
        self.appbar.actions = [
            ft.Container(
                content=popup_menu,
                margin=ft.margin.only(left=50, right=25)
            )
        ]
        
        self.page.appbar = self.appbar
        self.page.update()
     
if __name__ == "__main__":
 
    def main(page: ft.Page):
        page.title = "Flet Trello clone"
        page.padding = 0
        app = TrelloApp(page)
        page.add(app)
        page.update()
        page.update()
 
    ft.app(main)

