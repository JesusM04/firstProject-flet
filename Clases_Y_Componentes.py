import flet as ft

#DECLARACIONES DE VARIABLES GLOBALES, LISTAS Y CONTENEDOR PARA CONTROLAR EL FLUJO DEL PROGRAMA
global estado_ventana
global ventana_anterior
global datos_usuario
estado_ventana = 1
ventana_anterior = None
nombreA = None
apellidoA = None
pedidos = []


class Cliente:
    def __init__(self, id_cli, user_cli, pass_cli, nombre, apellido, pin):
        self.id_cli = id_cli
        self.user_cli = user_cli
        self.pass_cli = pass_cli
        self.nombre = nombre
        self.apellido = apellido
        self.pin = pin

    def __repr__(self):
        return f"Cliente(id_cli={self.id_cli}, user_cli='{self.user_cli}', nombre='{self.nombre}', apellido='{self.apellido}', pin='{self.pin})"

class Pedido:
    def __init__(self, id, tamano, estilo, tonalidades, material, tipo, precio, nombre_cliente, apellido_cliente, id_cli, user_cliente):
        self.id = id  # El id es autoincrementable en la base de datos
        self.tamano = tamano
        self.estilo = estilo
        self.tonalidades = tonalidades
        self.material = material
        self.tipo = tipo
        self.precio = precio  # Precio es un número real (float)
        self.nombre_cliente = nombre_cliente  # Nombre del cliente
        self.apellido_cliente = apellido_cliente  # Apellido del cliente
        self.user_cliente = user_cliente
        self.id_cli = id_cli  # id_cli es la clave foránea que hace referencia a la tabla clientes

    def __repr__(self):
        return (f"Pedido(id={self.id}, tamano='{self.tamano}', estilo='{self.estilo}', tonalidades='{self.tonalidades}', "
                f"material='{self.material}', tipo='{self.tipo}', precio={self.precio}, "
                f"nombre_cliente='{self.nombre_cliente}', apellido_cliente='{self.apellido_cliente}', id_cli={self.id_cli}', user_cliente={self.user_cliente})")

class Componentes:
    def __init__(self, page):
        self.page = page

    # Método para establecer dimensiones generales
    def establecer_dimensiones(self):
        self.page.window_width = 1200
        self.page.window_height = 740

    # Método para establecer dimensiones específicas para LOGIN
    def establecer_dimensionesLOGIN(self):
        self.page.window_width = 1200
        self.page.window_height = 740
        self.page.bgcolor = ft.colors.GREY_900

    def crearBusqueda():
        # Crear el botón de búsqueda (ícono Search)
        search_button = ft.IconButton(
            ft.icons.SEARCH,
            icon_size=30,
            icon_color=ft.colors.WHITE,
            data="ventana6",
            on_click=cambiar_ventana,
            tooltip="Ir a consultas"  # Agregar tooltip
        )

        # Crear el botón de logout
        logout_button = ft.IconButton(
            ft.icons.LOGOUT,
            icon_size=30,
            data="ventana1",
            on_click=cambiar_ventana,
            icon_color=ft.colors.WHITE,
            tooltip="Cerrar sesión"  # Agregar tooltip
        )

        # Fila principal: barra de búsqueda + ícono de búsqueda + botón logout
        search_row = ft.Row(
            controls=[
                search_button,  # Botón de búsqueda
                logout_button,  # Botón logout
            ],
            spacing=20,  # Espaciado entre los botones
            alignment=ft.MainAxisAlignment.CENTER,  # Centra los controles
        )

        # Devuelve el contenedor con los ajustes
        return ft.Container(
            content=search_row,  # Solo incluimos la fila con los botones
            width=1200,  # Ajusta el ancho del contenedor
            height=80,  # Ajusta la altura para incluir todos los elementos
            gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE_700, ft.colors.BLUE_700]),
            # bgcolor=ft.colors.BLUE_500,
            border_radius=10,
            padding=20,
        )