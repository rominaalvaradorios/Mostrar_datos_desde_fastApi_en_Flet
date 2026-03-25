import flet as ft
from styles.estilos import Buttons, Colors, Inputs, Textos_estilos, Card


def productos_view(page: ft.Page):

    titulo = ft.Text("Aplicación saludo", style=Textos_estilos.H1)
    subtitulo = ft.Text("Sistema con estilos", style=Textos_estilos.H2)

    nombre = ft.TextField(
        label="Nombre",
        **Inputs.INPUT_PRIMARY
    )

    mensaje_text = ft.Text("", style=Textos_estilos.H4)

    def on_click(e):
        mensaje_text.value = f"Hola {nombre.value}"
        page.update()

    btn = ft.Button(
        "Saludar",
        on_click=on_click,
        style=Buttons.BUTTON_PRIMARY
    )

    columna = ft.Column(
        controls=[titulo, subtitulo, nombre, btn, mensaje_text],
        spacing=16
    )

    card = ft.Container(
        content=columna,
        **Card.tarjeta
    )

    return ft.Container(
        padding=10,
        alignment=ft.Alignment(0, 0),
        content=card
    )
