import flet as ft
import time
from .categories import CategoriesView 

class Home:
    def __init__(self, page: ft.Page):
        self.page = page
        self.app_bar = None
        self.navigation_bar = None
        self.central_view = None
        self.initialize_components()

    def on_page_resized(self, e):
        if self.list_views:
            for list_view in self.list_views:
                list_view.on_page_resized(e)

    def update_search_field(self):
        if self.show_search:
            
            for i in range(0, 200):  
                self.app_bar.middle = ft.TextField(
                    hint_text="Search...",
                    border_radius=4,
                    border_color=ft.Colors.TRANSPARENT, 
                    bgcolor=ft.Colors.TRANSPARENT,
                    width=i,
                    height=30,
                    text_size=12,
                )
                self.app_bar.update() 
                time.sleep(0.001)  
             
        else: 
            SearhText = self.app_bar.middle.value
            if self.list_views[self.navigation_bar.selected_index]:
                self.list_views[self.navigation_bar.selected_index].search(SearhText)
                   
            self.app_bar.middle = ft.Text("Waver")   
            self.app_bar.update()   

       
        
        
    def initialize_components(self): 
        self.page.title = "Home"
        self.page.bgcolor ='#030303' # '#1A2229'  
        self.page.padding = ft.Padding(top=0, bottom=0, left=0, right=0) 
        self.list_views = [CategoriesView(self.page)]
        self.page.on_resized = self.on_page_resized 
        self.show_search = False 
         
        def toggle_search(e):
            self.show_search = not self.show_search  # Cambiar estado
            self.update_search_field()
            
        self.app_bar = ft.CupertinoAppBar(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, ft.Colors.WHITE, size=20),
            bgcolor=ft.Colors.TRANSPARENT,
            trailing=ft.IconButton(
                icon=ft.Icons.SEARCH_ROUNDED,
                icon_color=ft.Colors.WHITE,
                on_click=toggle_search,
                icon_size=20,
            ),
            middle=ft.Text("Waver"),
        )
 
        self.navigation_bar = ft.CupertinoNavigationBar( 
            bgcolor=ft.Colors.TRANSPARENT,   
           # indicator_color=ft.Colors.WHITE,
           # overlay_color='#212930', 
            height=50,
           #  surface_tint_color=ft.Colors.TRANSPARENT,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icon(ft.Icons.EXPLORE, '#5E6469', size=20), label="Explore"), 
                ft.NavigationBarDestination(icon=ft.Icon(ft.Icons.COMMUTE, '#5E6469', size=20) , label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.Icon(ft.Icons.BOOKMARK_BORDER, '#5E6469', size=20) ,  
                    label="Bookmarks",
                ),
            ],
            on_change=self.handle_navigation_change,
        )
 
        self.central_view = ft.Container(
            bgcolor=ft.Colors.TRANSPARENT,
            content=ft.Column(
                controls=[self.list_views[0].render()],
                expand=True,
                spacing=10,
                auto_scroll=False,
                scroll= ft.ScrollMode.ALWAYS, 
            ),
            expand=True, 
            alignment=ft.alignment.top_center,
            padding=ft.Padding(top=0, bottom=0, left=0, right=0), 
        )
         
        self.page.appbar = self.app_bar 
        # self.page.add(self.central_view) 
        # self.page.navigation_bar = self.navigation_bar 
     
        self.page.add(
            ft.Stack(
                controls=[ 
                    self.central_view,
                    ft.Container(
                        content=self.navigation_bar,
                        alignment=ft.alignment.bottom_center,
                        expand=False,
                        height=self.navigation_bar.height,
                        bottom=0,
                        left=0,
                        right=0,
                    ),
                ],
                expand=True,
            )
        ) 
         
    def handle_navigation_change(self, e):
        """Manejar el cambio de pestaña en la barra de navegación."""
        selected_index = e.control.selected_index 
        match selected_index:
            case 0:
                self.central_view.content =  self.list_views[0].render()
            case 1:
                self.central_view.content = ft.Text("Commute View")
            case 2:
                self.central_view.content = ft.Text("Bookmarks View")
        self.page.update()
  