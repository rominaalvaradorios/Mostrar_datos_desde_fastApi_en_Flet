import flet as ft
from typing import Any, Callable, Coroutine
from app.styles.estilos import Colors, Textos_estilos, Inputs, Buttons


def formulario_nuevo_editar_producto(
    page: ft.Page,
    on_submit: Callable[[dict], Coroutine],
    initial: dict | None = None,
):
    """
    Retorna una tupla (dlg, open_, close) donde:
      - dlg    : AlertDialog con el formulario
      - open_  : función para abrir el diálogo
      - close  : función para cerrar el diálogo
    Si initial es None  -> modo NUEVO producto.
    Si initial es un dict -> modo EDITAR (los campos se prellenan).
    """

    # ── Campos del formulario ─────────────────────────────────
    fld_name = ft.TextField(
        label="Nombre del producto",
        value=initial.get("name", "") if initial else "",
        **Inputs.INPUT_PRIMARY,
    )
    fld_quantity = ft.TextField(
        label="Cantidad",
        value=str(initial.get("quantity", "")) if initial else "",
        keyboard_type=ft.KeyboardType.NUMBER,
        **Inputs.INPUT_PRIMARY,
    )
    fld_ingreso = ft.TextField(
        label="Fecha de ingreso (YYYY-MM-DD)",
        value=initial.get("ingreso_date", "") if initial else "",
        **Inputs.INPUT_PRIMARY,
    )
    fld_min = ft.TextField(
        label="Stock mínimo",
        value=str(initial.get("min_stock", "")) if initial else "",
        keyboard_type=ft.KeyboardType.NUMBER,
        **Inputs.INPUT_PRIMARY,
    )
    fld_max = ft.TextField(
        label="Stock máximo",
        value=str(initial.get("max_stock", "")) if initial else "",
        keyboard_type=ft.KeyboardType.NUMBER,
        **Inputs.INPUT_PRIMARY,
    )

    # ── Función interna: cerrar diálogo ──────────────────────
    def close(_e=None):
        pop = getattr(page, "pop_dialog", None)
        if callable(pop):
            page.pop_dialog()
        page.update()

    # ── Función interna: guardar ──────────────────────────────
    async def guardar(_e):
        data: dict[str, Any] = {
            "name":         fld_name.value.strip(),
            "quantity":     int(fld_quantity.value or 0),
            "ingreso_date": fld_ingreso.value.strip() or None,
            "min_stock":    int(fld_min.value or 0),
            "max_stock":    int(fld_max.value or 0),
        }
        close()
        await on_submit(data)

    # ── Dialog ───────────────────────────────────────────────
    titulo = "Editar producto" if initial else "Nuevo producto"

    dlg = ft.AlertDialog(
        modal=True,
        title_padding=0,
        content_padding=0,
        title=ft.Container(
            bgcolor=Colors.PRIMARY,
            padding=12,
            border_radius=ft.BorderRadius(18, 18, 0, 0),
            content=ft.Text(titulo, color=Colors.WHITE, weight=ft.FontWeight.BOLD),
        ),
        content=ft.Container(
            padding=20,
            content=ft.Column(
                tight=True,
                spacing=14,
                controls=[
                    fld_name,
                    fld_quantity,
                    fld_ingreso,
                    fld_min,
                    fld_max,
                ],
            ),
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=close),
            ft.Button(
                "Guardar",
                icon=ft.Icons.SAVE,
                on_click=guardar,
                style=Buttons.BUTTON_SUCCESS,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_():
        page.show_dialog(dlg)

    return dlg, open_, close
