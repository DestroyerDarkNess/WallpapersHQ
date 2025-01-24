import flet as ft
import random
# from core.widgets import Carousel, Card, ModernCarousel
from core import WallhavenScraper, Ratio

class CategoriesView:
     
    def __init__(self, page: ft.Page):
        self.page = page
        self.column_count = 2
        self.spacing = 10
        self.min_card_width = 200
        self.images = []             # Guardaremos aquí las imágenes para refrescar en el resize
        self.Content = self.initialize_components()

    def render(self):
        return self.Content

    def card_clicked(self, index: int):
        print(f"Se hizo clic en la tarjeta con índice {index}")

    def on_card_click(self, e): 
        print(f"Se hizo clic en la tarjeta con URL {e.control.data}")
        
    def more_like(self, e): 
        base_url = e.control.parent.content.src
        base_id = self.scraper.get_image_id(base_url)
        self.search(f"like:{base_id}") 

    def initialize_components(self): 
        self.scraper = WallhavenScraper() 
        self.images = self.scraper.get_images(self.scraper.random )
 
        self.masonry_layout = ft.Row(spacing =self.spacing, alignment=ft.MainAxisAlignment.CENTER )
         
        main_column = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Container(height=30),
                self.masonry_layout,
                ft.Container(height=50),
            ],
        )
         
        self.list_images(self.images)
   
        return main_column

    def list_images(self, images=None): 
        if not images:
            return
 
        self.column_count = max(2, int(self.page.window_width // (self.min_card_width + self.spacing)))
 
        self.columns = [ft.Column(spacing=10) for _ in range(self.column_count)]
 
        total_spacing = self.spacing * (self.column_count + 1)
        card_width = (self.page.window_width - total_spacing) / self.column_count

        for idx, img_info in enumerate(images):
            card_height = random.randint(200, 300)  
            
            image = ft.Image(
                src=img_info.minimized_img,
                fit=ft.ImageFit.COVER,
                width=card_width,
                height=card_height,
                border_radius=ft.border_radius.all(8),
            )
            
            ContextMenu = ft.CupertinoContextMenu(
                enable_haptic_feedback=True,
                content=image,
                actions=[
                    ft.CupertinoContextMenuAction( 
                        text="More like this",
                        is_default_action=True,
                        trailing_icon=ft.Icons.HEART_BROKEN_SHARP,
                        on_click=self.more_like,
                    ),
                    ft.CupertinoContextMenuAction(
                        text="Action 2",
                        trailing_icon=ft.Icons.MORE,
                        on_click=lambda e: print("Action 2"),
                    ),
                    ft.CupertinoContextMenuAction(
                        text="Action 3",
                        is_destructive_action=True,
                        trailing_icon=ft.Icons.CANCEL,
                        on_click=lambda e: print("Action 3"),
                    ),
                ],
            )
             
            card = ft.Container(
                bgcolor=ft.colors.AMBER_100,
                data=img_info.minimized_img,
                on_click=self.on_card_click,
                content=ContextMenu,
                width=image.width,
                height=image.height,
                border_radius=image.border_radius,
                padding=1,
            )
 
            self.columns[idx % self.column_count].controls.append(card)
 
        self.masonry_layout.controls = self.columns
 
    def on_page_resized(self, e):  
        self.list_images(self.images)
        self.page.update()
        
    def search(self, text):  
        self.masonry_layout.controls = []
        self.masonry_layout.update()
        
        if text:
            self.images = self.scraper.get_images(
                self.scraper.make_search(text, page=1, ratios=Ratio.ALL)
            )
        else:
            self.images = self.scraper.get_images(self.scraper.random)
                
        if self.scraper.error_connection == True:
            self.page.snack_bar = ft.SnackBar(ft.Text("No connection"))
            self.page.snack_bar.open = True
        elif len(self.images) == 0:
            # self.page.snack_bar = ft.SnackBar(ft.Text("No results"))
            # self.page.snack_bar.open = True
            
            def handle_action_click(e):
                self.page.close(e.control.parent)
                self.images = self.scraper.get_images(self.scraper.random) 
                self.list_images(self.images)
                self.page.update()
        
            cupertino_actions = [
                    ft.CupertinoDialogAction(
                        "OK",
                        is_destructive_action=True,
                        on_click=handle_action_click,
                    )
                ]
              
            self.page.open(ft.CupertinoAlertDialog(
                                title=ft.Text("No results found"),
                                content=ft.Text("Don't worry, I'll look for other wallpapers for you."),
                                actions=cupertino_actions,
                            ))
        else:
            self.list_images(self.images)
        self.page.update()
        
