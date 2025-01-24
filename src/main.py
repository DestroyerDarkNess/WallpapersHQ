# program.py
import flet as ft
from views import Home
 
class Program:
    def start(self, page: ft.Page): 
        page.title = "Waver"
        page.window.left = 980
        page.window.top = 5
        page.window.width = 390
 
        home = Home(page)
        page.update()
 
if __name__ == "__main__":
    ft.app(target=Program().start)
     
# def main(page: ft.Page):
#     page.add(
#         ft.InteractiveViewer(
#             min_scale=0.1,
#             max_scale=15,
#             boundary_margin=ft.margin.all(20),
#             on_interaction_start=lambda e: print(e),
#             on_interaction_end=lambda e: print(e),
#             on_interaction_update=lambda e: print(e),
#             content=ft.Image(
#                 src="https://picsum.photos/500/500",
#             ),
#         )
#     )


# ft.app(main)
 
  
