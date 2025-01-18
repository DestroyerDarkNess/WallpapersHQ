import flet as ft

class Home:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_bar = None
        self.navigation_bar = None
        self.central_view = None
        self.initialize_components()

    def initialize_components(self):
        # Configurar el tema
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.title = "Home"

        # Configurar el CupertinoAppBar
        self.app_bar = ft.CupertinoAppBar(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
            bgcolor=ft.Colors.SURFACE,
            trailing=ft.Icon(ft.Icons.SEARCH_ROUNDED),
            middle=ft.Text("Waver"),
        )

        # Configurar el NavigationBar
        self.navigation_bar = ft.NavigationBar(
            bgcolor=ft.Colors.TRANSPARENT,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Bookmarks",
                ),
            ],
            on_change=self.handle_navigation_change,
        )
 
        self.central_view = ft.Container(
            content=ft.Text("Welcome to the Home Screen!"),
            expand=True,
            alignment=ft.alignment.center,
        )
 
        self.page.appbar = self.app_bar
        self.page.navigation_bar = self.navigation_bar
        self.page.add(self.central_view)

    def handle_navigation_change(self, e):
        """Manejar el cambio de pestaña en la barra de navegación."""
        selected_index = e.control.selected_index
        match selected_index:
            case 0:
                self.central_view.content = ft.Text("Explore View")
            case 1:
                self.central_view.content = ft.Text("Commute View")
            case 2:
                self.central_view.content = ft.Text("Bookmarks View")
        self.page.update()


# if __name__ == "__main__": 
#     def main(page: ft.Page):
#         home = Home(page)

#     ft.app(main)

# def debugging_view(page: ft.Page):
#     return Home(page)
