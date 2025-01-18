# program.py
import flet as ft
from views import Home

class Program:
    def start(self, page: ft.Page): 
        page.title = "Waver"
        page.window_left = 980
        page.window_top = 5
        page.window.width = 390
 
        home = Home(page)
        page.update()

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=Program().start)
