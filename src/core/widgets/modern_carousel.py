import flet as ft
from typing import List, Callable, Optional
import random

class Card:
    def __init__(
        self,
        image_url: str,
        width: float = 300,
        height: float = 200,
        border_radius: float = 12
    ):
        self.image_url = image_url
        self.width = width
        self.height = height
        self.border_radius = border_radius


class ModernCarousel(ft.UserControl):
    """
    Carrusel moderno con callback externo para evento on_card_click.
    """
    def __init__(
        self,
        cards: List[Card],
        shuffle: bool = False,
        width: float = None,
        height: float = None,
        active_dot_color: str = ft.colors.WHITE,
        inactive_dot_color: str = ft.colors.WHITE54,
        on_card_click: Optional[Callable[[int], None]] = None, 
        # ^^^^^^^^^^
        # Este callback (función) se llamará cuando el usuario haga clic en una tarjeta.
        # Recibe el índice int de la tarjeta clicada.
    ):
        super().__init__()
        self.cards = cards
        if shuffle:
            self.cards = random.sample(self.cards, len(self.cards))

        self.width = width
        self.height = height
        self.current_index = 0
        self.active_dot_color = active_dot_color
        self.inactive_dot_color = inactive_dot_color
 
        self.on_card_click = on_card_click
 
        self.card_container_ref = ft.Ref[ft.Container]()
        self.dot_row_ref = ft.Ref[ft.Row]()

    def build(self):
        return ft.Container(
            width=self.width,
            height=self.height,
            expand=(self.width is None and self.height is None),
            alignment=ft.alignment.center,
            content=ft.GestureDetector(
                on_horizontal_drag_end=self.handle_swipe,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Container(
                            ref=self.card_container_ref,
                            alignment=ft.alignment.center,
                            animate_opacity=300,
                        ),
                        ft.Row(
                            ref=self.dot_row_ref,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        )
                    ],
                ),
            ),
        )

    def did_mount(self):
        self._load_card(self.current_index, animate=False)
        self._load_dots()
        self.update()

    def handle_swipe(self, e: ft.DragEndEvent):
        if e.primary_velocity < 0:
            self.current_index = (self.current_index + 1) % len(self.cards)
        elif e.primary_velocity > 0:
            self.current_index = (self.current_index - 1) % len(self.cards)

        self._load_card(self.current_index, animate=True)
        self._update_dots()

    def _on_dot_clicked(self, e):
        index = e.control.data
        self.current_index = index
        self._load_card(index, animate=True)
        self._update_dots()

    def _on_card_tap(self, e: ft.TapEvent):
        """
        Este método interno se llama cuando se da clic en la tarjeta actual.
        Luego invoca el callback externo (on_card_click) si está definido.
        """
        index = e.control.data  # índice de la tarjeta
        if self.on_card_click is not None:
            self.on_card_click(index)

    def _load_card(self, index: int, animate: bool = True):
        if animate:
            self.card_container_ref.current.opacity = 0
            self.update()

        card = self.cards[index]

        # Escalado responsivo
        if self.width and self.height:
            w_scale = self.width * 0.8
            h_scale = self.height * 0.8
            card_ratio = card.width / card.height if card.height != 0 else 1

            new_width = w_scale
            new_height = w_scale / card_ratio

            if new_height > h_scale:
                new_height = h_scale
                new_width = h_scale * card_ratio
        else:
            new_width = card.width
            new_height = card.height

        # Envolvemos la imagen en un GestureDetector que llame a _on_card_tap
        card_gesture = ft.GestureDetector(
            data=index,  # pasamos el índice
            on_tap=self._on_card_tap,
            content=ft.Image(
                src=card.image_url,
                fit=ft.ImageFit.COVER,
                width=new_width,
                height=new_height,
                border_radius=ft.border_radius.all(card.border_radius),
            ),
        )

        # Actualizamos el contenedor
        self.card_container_ref.current.width = new_width
        self.card_container_ref.current.height = new_height
        self.card_container_ref.current.border_radius = ft.border_radius.all(card.border_radius)
        self.card_container_ref.current.content = card_gesture

        if animate:
            self.card_container_ref.current.opacity = 1
            self.update()

    def _load_dots(self):
        self.dot_row_ref.current.controls.clear()

        for i in range(len(self.cards)):
            dot_gesture = ft.GestureDetector(
                data=i,
                on_tap=self._on_dot_clicked,
                content=ft.Container(
                    width=12 if i == self.current_index else 8,
                    height=8,
                    border_radius=8,
                    bgcolor=self.active_dot_color if i == self.current_index else self.inactive_dot_color,
                    animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                )
            )
            self.dot_row_ref.current.controls.append(dot_gesture)

        self.dot_row_ref.current.update()

    def _update_dots(self):
        for i, dot_gesture in enumerate(self.dot_row_ref.current.controls):
            dot_container = dot_gesture.content
            dot_container.width = 12 if i == self.current_index else 8
            dot_container.bgcolor = (
                self.active_dot_color
                if i == self.current_index
                else self.inactive_dot_color
            )
        self.update()
