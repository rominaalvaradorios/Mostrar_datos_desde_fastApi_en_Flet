import flet as ft

# importamos todos los estilos
from styles.estilos import Buttons, Card, Colors, Inputs, Textos_estilos

# importamos los tipos de mensajes
from components.popup import show_popup, show_popup_auto_close, show_snackbar


def main(page: ft.Page):

    # Crear el texto para el titulo
    title = ft.Text(
        "Mi app Flet",
        style=Textos_estilos.H4,
        text_align=ft.TextAlign.CENTER
    )

    # Crear el texto para el subtitulo
    subtitle = ft.Text(
        "Sistema de estilos centralizado",
        style=Textos_estilos.H5
    )

    # Caja de texto para pedir el nombre
    name = ft.TextField(
        label="Nombre",
        **Inputs.INPUT_PRIMARY
    )

    # Funcionalidad del botón
    async def on_click(e):

        titulo = "Saludo"
        mensaje = f"Hola {name.value}"

        await show_popup(page, titulo, mensaje, Colors.PRIMARY, Colors.WHITE)
        #Mostrar el mensaje 
        #Descomenta primero el show_popup, luego show_popup-auto_close y asi sucesivamente, para ver como funciona
        #await show_popup(page, titulo, mensaje, Colors.PRIMARY, Colors.WHITE)
        #show_popup_auto_close cierra en automatico tras 3 segundos
        #await show_popup_auto_close(page, titulo, mensaje, Colors.PRIMARY, Colors.WHITE, 3
        #await show_snackbar(page, titulo, mensaje, Colors.PRIMARY, Colors.WHITE)
        
    # Crear botón
    btn = ft.ElevatedButton(
        "Saludar",
        on_click=on_click,
        style=Buttons.BUTTON_PRIMARY
    )

    # Mostrar componentes
    page.add(title, subtitle, name, btn)


if __name__ == "__main__":
    ft.run(main)