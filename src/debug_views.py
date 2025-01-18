import flet as ft
from views.categories import debugging_view
# from views.home import debug_view

def main(page: ft.Page):
    page.add(debugging_view(page))
    page.update()
ft.app(main)