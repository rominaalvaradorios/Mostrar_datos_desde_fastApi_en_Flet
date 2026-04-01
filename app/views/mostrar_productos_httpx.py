import flet as ft
from typing import Any
from app.services.transacciones_api_productos_httpx import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos, Card
from app.views.nuevo_editar import formulario_nuevo_editar_producto #Se agrega la ventana de nuevo/editar

def products_view(page:ft.Page) -> ft.Control:
    ############# Nuevo producto ##############
    #Esta función se ejecuta al hacer click en "Nuevo producto"
    #lo que hace en primer lugar es abrir la ventana para captura de datos
    def inicio_nuevo_producto(_e):
        #Se crea la función para transferir al formulario de nuevo producto
        async def crear_nuevo_producto(data:dict):#Esta función se lleva a la ventana para capturar
            try:
                #Se conecta a transacciones_api_productos.py para crear en la BD un nuevo produto
                await create_product(data)
                await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)
                
        #Se llama a la función para abrir la ventana y poder capturar los datos,
        # regresa 3 funciones(dlg,open_ y close), se ejecuta open_()
        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_() #Abre la ventana
    ############ FIN nuevo producto ############
    btn_nuevo = ft.Button("Nuevo producto",icon=ft.Icons.ADD,on_click=inicio_nuevo_producto)

    rows_data: list[dict[str, Any]] = []
    total_items = 0
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos_estilos.H4)

    # ── Encabezados de la tabla ──────────────────────────────
    columnas = [
        ft.DataColumn(label=ft.Text("Nombre",  style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Ingreso",  style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Min",      style=Textos_estilos.H4)),
        ft.DataColumn(label=ft.Text("Max",      style=Textos_estilos.H4)),
    ]

    # Fila de placeholder mientras se cargan los datos
    data = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("cargando...")),
                ft.DataCell(ft.Text("-")),
                ft.DataCell(ft.Text("-")),
                ft.DataCell(ft.Text("-")),
                ft.DataCell(ft.Text("-")),
            ]
        )
    ]

    # ── Tabla ────────────────────────────────────────────────
    tabla = ft.DataTable(
        columns=columnas,
        rows=data,
        width=900,
        heading_row_height=60,
        heading_row_color=Colors.BG,
        data_row_max_height=60,
        data_row_min_height=48,
    )

    # ────────────────────────────────────────────────────────
    # Función actualizar_data()
    #   - Se conecta a transacciones_api_productos_httpx.py para
    #     solicitar el listado de productos desde FastAPI.
    #   - Recupera el total de items en total_items.
    #   - Recupera los registros en rows_data.
    # ────────────────────────────────────────────────────────
    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            # Parte 1 ▸ llamada al servicio async (GET /products/)
            data = await list_products(limit=500, offset=0)

            # Parte 2 ▸ recuperar total e items
            total_items = int(data.get("total", 0))
            total_text.value = "Total de productos: " + str(total_items)
            rows_data = data.get("items", []) or []

            # Parte 3 ▸ actualizar las filas de la tabla
            actualizar_filas()
        except Exception as ex:
            await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

    # ────────────────────────────────────────────────────────
    # Función actualizar_filas()
    #   - Extrae los registros de rows_data.
    #   - Actualiza las filas dentro de la tabla de Flet.
    # ────────────────────────────────────────────────────────
    def actualizar_filas():
        nuevas_filas = []
        for p in rows_data:
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.get("name", ""))),
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", "") or "")),
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()

    # Ejecuta la carga de datos al iniciar la vista
    page.run_task(actualizar_data)

    contenido = ft.Column(
        #expand=True,
        spacing=30,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            btn_nuevo,
            total_text,
            ft.Container(content=tabla)
        ]
    )
    tarjeta = ft.Container(content=contenido,**Card.tarjeta)

    return tarjeta
