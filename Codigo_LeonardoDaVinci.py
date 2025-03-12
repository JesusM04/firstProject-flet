import flet as ft
import sqlite3
import random
from BaseDeDatos import *
from Clases_Y_Componentes import *

def main(page: ft.Page):
    #DIMENSIONES DE LAS VENTANAS
    page.title = "LEONARDO DA VINCI"

    #INICIALIZACION DE BD
    gestor = GestorPedidos()
    gestor.init_db()
    #INICIALIZACION DE LAS CLASES Y COMPONENTES
    componentes = Componentes(page)

    # Lista que almacenará los PINs generados para la sesión actual
    pins_generados = []

    def generar_pin_unico():
        """Genera un PIN único aleatorio entre 1000 y 9999."""
        while True:
            pin = random.randint(1000, 9999)  # Genera un PIN de 4 dígitos
            # Verificamos que el PIN no haya sido generado anteriormente
            if pin not in pins_generados:
                pins_generados.append(pin)  # Añadimos el PIN a la lista
                return pin  # Retornamos el PIN único generado

    def seleccionar_pedido(pedido_id):
        global selected_pedido
        selected_pedido = pedido_id
        print(f"Pedido seleccionado: {selected_pedido}")

    def last10_view(usuario, tipo):
        list_view = ft.ListView(expand=True, spacing=10, padding=20)

        # Obtener todos los pedidos de la base de datos
        pedidos = gestor.obtener_pedidos_db(usuario, tipo)

        # Ordenar los pedidos por ID en orden descendente
        pedidos_ordenados = sorted(pedidos, key=lambda x: x[0], reverse=True)

        # Tomar los últimos 10 pedidos
        ultimos_10_pedidos = pedidos_ordenados[:10]

        for pedido in ultimos_10_pedidos:
            pedido_id, tamano, estilo, tonalidades, material, tipo, precio, nombre_cliente, apellido_cliente, user_cliente = pedido
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Pedido #{pedido_id}: {tamano} - {estilo}"),
                    subtitle=ft.Text(
                        f"Tonalidades: {tonalidades} | Material: {material} | Tipo: {tipo}\n| Precio: ${precio:.2f} | Cliente: {nombre_cliente} {apellido_cliente} | Usuario: {user_cliente}"
                    ),
                    trailing=ft.Icon(
                        ft.Icons.CHECK_CIRCLE if precio else ft.Icons.PENDING,
                        color=ft.Colors.GREEN if precio else ft.Colors.RED
                    ),
                    on_click=lambda e, pedido_id=pedido_id: seleccionar_pedido(pedido_id),
                    # Este código no está tratando con 'artista'
                )
            )

        return list_view

    def mostrar_pedidos_en_listview(usuario, tipo):
        list_view = ft.ListView(expand=True, spacing=10, padding=20)

        pedidos = gestor.obtener_pedidos_db(usuario, tipo)
        for pedido in pedidos:
            # El loop agrega cada pedido al ListView
            pedido_id, tamano, estilo, tonalidades, material, tipo, precio, nombre_cliente, apellido_cliente, user_cliente = pedido
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Pedido #{pedido_id}: {tamano} - {estilo}"),
                    subtitle=ft.Text(
                        f"Tonalidades: {tonalidades} | Material: {material} | Tipo: {tipo}\n| Precio: ${precio:.2f} | Cliente: {nombre_cliente} {apellido_cliente} | Usuario: {user_cliente}"
                    ),
                    trailing=ft.Icon(ft.Icons.CHECK_CIRCLE if precio else ft.Icons.PENDING,
                                     color=ft.Colors.GREEN if precio else ft.Colors.RED),
                    on_click=lambda e, pedido_id=pedido_id: seleccionar_pedido(pedido_id),
                )
            )

        # Aquí no se hace ninguna condición de retorno, por lo que la función termina sin ningún contenedor
        return list_view

    def mostrar_pedidos_sin_precio(usuario, tipo):
        list_view = ft.ListView(expand=True, spacing=10, padding=20)

        # Obtener todos los pedidos de la base de datos
        pedidos = gestor.obtener_pedidos_con_precio_0(usuario, tipo)

        for pedido in pedidos:
            pedido_id, tamano, estilo, tonalidades, material, tipo, precio, nombre_cliente, apellido_cliente, user_cliente = pedido
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"Pedido #{pedido_id}: {tamano} - {estilo}"),
                    subtitle=ft.Text(
                        f"Tonalidades: {tonalidades} | Material: {material} | Tipo: {tipo}\n| Precio: ${precio:.2f} | Cliente: {nombre_cliente} {apellido_cliente} | Usuario: {user_cliente}"
                    ),
                    trailing=ft.Icon(ft.Icons.CHECK_CIRCLE if precio else ft.Icons.PENDING,
                                     color=ft.Colors.GREEN if precio else ft.Colors.RED),
                    on_click=lambda e, pedido_id=pedido_id: seleccionar_pedido(pedido_id),
                )
            )

        return list_view

    def cambiar_ventana(e):
        global estado_ventana
        global ventana_anterior

        nombre_ventana = e.control.data  # Obtiene el nombre de la ventana desde el botón
        page.controls.clear()  # Limpia los controles actuales

        # Depuración: Verifica el valor de estado_ventana antes de cambiarlo

        if nombre_ventana == "ventana1":
            estado_ventana = 1
            page.controls.append(ventanaLogin())
        elif nombre_ventana == "ventana2":
            estado_ventana = 2
            page.controls.append(ventanaRegistro())
        elif nombre_ventana == "ventana3":
            estado_ventana = 3
            page.controls.append(ventanaReestablecerPassword())
        elif nombre_ventana == "ventana4":
            estado_ventana = 4  # Cambiar el estado correctamente
            page.controls.append(ventanaArtista())
        elif nombre_ventana == "ventana5":
            estado_ventana = 5
            page.controls.append(ventanaCliente())
        elif nombre_ventana == "ventana6":
            estado_ventana = 6
            page.controls.append(ventanaConsultas())
        elif nombre_ventana == "ventana7":
            estado_ventana = 7
            page.controls.append(ventanaResumen())

        # Asegúrate de que page.update() se llama solo una vez, al final
        page.update()

    def crearBusqueda():
        global estado_ventana
        global ventana_anterior

        # Crear los botones
        search_button = ft.IconButton(
            ft.icons.SEARCH,
            icon_size=30,
            icon_color=ft.colors.WHITE,
            data="ventana6",
            on_click=cambiar_ventana,
            tooltip="Ir a consultas"
        )

        logout_button = ft.IconButton(
            ft.icons.LOGOUT,
            icon_size=30,
            data="ventana1",
            on_click=cambiar_ventana,
            icon_color=ft.colors.WHITE,
            tooltip="Cerrar sesión"
        )

        resumen_button = ft.IconButton(
            ft.icons.ACCOUNT_BALANCE,
            icon_size=30,
            data="ventana7",
            on_click=cambiar_ventana,
            icon_color=ft.colors.WHITE,
            tooltip="Ver resumen de empresa"
        )

        usuario_button = ft.IconButton(
            ft.icons.PERSON,
            icon_size=30,
            data="ventana4" if ventana_anterior == 4 else "ventana5",  # Cambio aquí
            on_click=cambiar_ventana,
            icon_color=ft.colors.WHITE,
            tooltip="Volver a ventana anterior"
        )

        # Verifica el valor de estado_ventana antes de asignar search_row_controls
        print(f"Estado de la ventana en crearBusqueda: {estado_ventana}")

        # Inicializar search_row_controls
        search_row_controls = []

        # Asignar los controles según el estado actual
        if estado_ventana == 7:
            search_row_controls = [search_button, usuario_button, logout_button]
        elif estado_ventana == 4:
            search_row_controls = [search_button, resumen_button, logout_button]
        #elif estado_ventana == 6:
         #   search_row_controls = [search_button, logout_button]
        elif estado_ventana == 5:
            search_row_controls = [search_button, logout_button]

        # Crear la fila con los controles seleccionados
        search_row = ft.Row(
            controls=search_row_controls,
            spacing=20,  # Espaciado entre los botones
            alignment=ft.MainAxisAlignment.CENTER,  # Centra los controles
        )

        # Crear y devolver el contenedor
        return ft.Container(
            content=search_row,
            width=1200,
            height=80,
            gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE_700, ft.colors.BLUE_700]),
            border_radius=10,
            padding=20,
        )

    # Ventana 1: Inicio de sesión
    def ventanaLogin():

        componentes.establecer_dimensionesLOGIN()
        password_visible = False
        max_length = 9

        def on_login_clicked(e):  # Funcion para manejar el evento del boton
            global nombreA, apellidoA
            if not user_text_field.value or not password_text_field.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor, complete todos los datos."),
                    action="Cerrar"
                )
                page.snack_bar.open = True  # Mostrar el SnackBar
                page.update()  # Actualizar la página
                return  # Salir de la función sin continuar

            resultado = ""
            resultado = gestor.manejar_click(user_text_field.value, password_text_field.value, page)  # Llamar a manejar_clic pasando page

            if resultado:
                # Si el resultado es verdadero (credenciales correctas), obtenemos el nombre y apellido
                datos_usuario = gestor.obtener_datos_usuario(user_text_field.value, password_text_field.value, page)
                # Extraemos el nombre y apellido del diccionario
                nombreA = datos_usuario.get("nombre")  # Usamos get() por si la clave no existe
                apellidoA = datos_usuario.get("apellido")
                e.control.data = resultado  # Asignar a data el resultado
                page.session.set("usuario", user_text_field.value)  # Guarda el ID del usuario en la sesión
                # Ahora pasamos nombre y apellido a la función cambiar_ventana solo si es ventana5
                if e.control.data == "ventana5":  # Comprobar si es la ventana 5
                    cambiar_ventana(e)
                else:
                    e.control.data = "ventana4"
                    cambiar_ventana(e)  # Llamar a cambiar_ventana sin parámetros adicionales

                #cambiar_ventana(e)  # Llamar a cambiar_ventana
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña incorrectos"))
                page.snack_bar.open = True
                page.update()


        # Función para alternar visibilidad de la contraseña
        def toggle_password_visibility(e):
            nonlocal password_visible
            password_visible = not password_visible
            password_text_field.password = not password_visible
            toggle_button.icon = ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF
            page.update()

        # Metodo para manejar el cambio de la contraseña y el contador de caracteres restantes
        def on_password_change(e):
            remaining_chars_text.value = f"Caracteres restantes: {max_length - len(password_text_field.value)}"
            page.update()

        # Crear los componentes que se necesitan actualizar
        password_text_field = ft.TextField(
            label="Contraseña", hint_text="Contraseña", width=240, prefix_icon=ft.icons.LOCK,
            password=not password_visible, max_length=max_length, on_change=on_password_change,
        )

        user_text_field = ft.TextField(
            label="@user", hint_text="Usuario", width=280, prefix_icon=ft.icons.PERSON,
        )

        toggle_button = ft.IconButton(
            icon=ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF,
            on_click=toggle_password_visibility, tooltip="Ver contraseña"  # Agregar tooltip
        )

        remaining_chars_text = ft.Text(f"Caracteres restantes: {max_length}", size=12, color=ft.colors.BLACK)

        # Contenedor con todo
        return ft.Container(
            ft.Column([
                ft.Text("Iniciar Sesión", size=30, text_align="center", weight="900", width=280, font_family="Helvetica"),
                user_text_field,

                # Contenedor para la contraseña
                ft.Row([
                    password_text_field, toggle_button
                ], alignment=ft.MainAxisAlignment.START),

                # Muestra de caracteres restantes
                remaining_chars_text,

                ft.ElevatedButton(
                    text="Reestablecer contraseña", width=280, bgcolor="black", data="ventana3",
                    on_click=cambiar_ventana # Llamar a la funcion on_login_clicked
                ),
                ft.ElevatedButton(
                    text="Iniciar", width=280, bgcolor="black", data=on_login_clicked,
                    on_click=on_login_clicked  # Llamar a la funcion on_login_clicked
                ),
                ft.Text("Iniciar sesión con", text_align="center", font_family="Helvetica", width=285),
                ft.Row([ft.IconButton(icon=ft.icons.EMAIL), ft.IconButton(icon=ft.icons.FACEBOOK),
                        ft.IconButton(icon=ft.icons.APPLE)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([ft.Text("¿No tienes cuenta?"), ft.TextButton("Crear cuenta", data="ventana2", on_click=cambiar_ventana)],
                       alignment=ft.MainAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            border_radius=20, width=320, height=600,
            gradient=ft.LinearGradient([ft.colors.PURPLE, ft.colors.BLUE, ft.colors.PURPLE]),
            padding=ft.padding.only(20)
        )

    # Ventana 2: Registro
    def ventanaRegistro():
        componentes.establecer_dimensionesLOGIN()
        password_visible = False
        max_length = 9

        # Generar el PIN de recuperación
        pin_recuperacion = generar_pin_unico()

        # Función para alternar visibilidad de la contraseña
        def toggle_password_visibility(e):
            nonlocal password_visible
            password_visible = not password_visible
            password_text_field.password = not password_visible
            password_text_field2.password = not password_visible
            toggle_button.icon = ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF
            toggle_button2.icon = ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF
            page.update()

        # Función para manejar el cambio de la contraseña y el contador de caracteres restantes
        def on_password_change(e):
            remaining_chars_text.value = f"Caracteres restantes: {max_length - len(password_text_field.value)}"
            page.update()

        # Función para manejar el clic en "Completar"
        def on_complete_click(e):
            if not (
                    nombre_text_field.value and apellido_text_field.value and user_text_field.value and password_text_field.value and password_text_field2.value):
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor, complete todos los datos."),
                    action="Cerrar"
                )
                page.snack_bar.open = True
            else:
                # Crear una instancia de Cliente con los datos del formulario
                cliente = Cliente(
                    id_cli=None,
                    user_cli=user_text_field.value,  # Usar el correo electrónico como el nombre de usuario
                    pass_cli=password_text_field.value,
                    nombre=nombre_text_field.value,
                    apellido=apellido_text_field.value,
                    pin=pin_recuperacion
                )

                # Guardar los datos en la base de datos (llamar al método de gestor para guardar)
                resultado = gestor.guardar_credenciales(cliente.user_cli, cliente.pass_cli, cliente.nombre,
                                                        cliente.apellido, cliente.pin)

                if resultado["status"] == "error":
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(resultado["message"]),
                        action="Cerrar"
                    )
                    page.snack_bar.open = True
                elif resultado["status"] == "success":
                    # Actualizar el campo del PIN de recuperación
                    recovery_pin_text_field.value = pin_recuperacion
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([
                            ft.Text(f"Registro exitoso. Su PIN de recuperación es: {pin_recuperacion}. "),
                            ft.TextButton(
                                "Iniciar sesión ahora",
                                on_click=cambiar_ventana,
                                data="ventana1",
                            )
                        ]),
                        action="Cerrar",
                        duration=5000  # Durará 5 segundos en pantalla
                    )
                    page.snack_bar.open = True

                page.update()

            page.update()

        # Crear los componentes que se necesitan actualizar
        nombre_text_field = ft.TextField(label="Nombre", hint_text="Ingrese su nombre", width=280,
                                         prefix_icon=ft.icons.PERSON)
        apellido_text_field = ft.TextField(label="Apellido", hint_text="Ingrese su apellido", width=280,
                                           prefix_icon=ft.icons.PERSON)
        user_text_field = ft.TextField(label="Usuario", hint_text="@user", width=280,
                                        prefix_icon=ft.icons.PERSON)
        password_text_field = ft.TextField(
            label="123456", hint_text="Ingrese su contraseña", width=240, prefix_icon=ft.icons.LOCK,
            password=not password_visible, max_length=max_length, on_change=on_password_change
        )
        password_text_field2 = ft.TextField(
            label="123456", hint_text="Ingrese nuevamente su contraseña", width=240, prefix_icon=ft.icons.LOCK,
            password=not password_visible, max_length=max_length, on_change=on_password_change
        )
        toggle_button = ft.IconButton(
            icon=ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF,
            on_click=toggle_password_visibility
        )
        toggle_button2 = ft.IconButton(
            icon=ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF,
            on_click=toggle_password_visibility
        )
        remaining_chars_text = ft.Text(f"Caracteres restantes: {max_length}", size=12, color=ft.colors.BLACK)

        # Campo de texto para mostrar el PIN de recuperación
        recovery_pin_text_field = ft.TextField(
            label="Recuerde recordar y guardar este PIN",
            value="",  # Inicialmente vacío
            width=280,
            prefix_icon=ft.icons.LOCK,
            disabled=True  # Campo bloqueado
        )

        # Contenedor con todo
        return ft.Container(
            ft.Column([
                ft.Text("Registrarse", size=30, text_align="center", weight="900", width=280, font_family="Helvetica"),
                nombre_text_field, apellido_text_field, user_text_field,

                # Contenedor para la contraseña
                ft.Row([
                    password_text_field, toggle_button,
                ], alignment=ft.MainAxisAlignment.START),

                ft.Row([
                    password_text_field2,
                ], alignment=ft.MainAxisAlignment.START),

                # Campo del PIN de recuperación
                recovery_pin_text_field,

                # Muestra de caracteres restantes
                remaining_chars_text,

                ft.ElevatedButton(text="Completar", width=280, bgcolor="black", on_click=on_complete_click),
                ft.ElevatedButton(text="Volver a Login", width=280, bgcolor="black", data="ventana1",
                                  on_click=cambiar_ventana)

            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            border_radius=20, width=320, height=600,
            gradient=ft.LinearGradient([ft.colors.PURPLE, ft.colors.BLUE, ft.colors.PURPLE]),
            padding=ft.padding.only(20)
        )

    def ventanaReestablecerPassword():
        componentes.establecer_dimensionesLOGIN()
        max_pin_length = 4
        max_password_length = 9
        password_visible = False

        # Función para alternar visibilidad de las contraseñas
        def toggle_password_visibility(e):
            nonlocal password_visible
            password_visible = not password_visible
            nueva_password_field.password = not password_visible
            confirmar_password_field.password = not password_visible
            toggle_button.icon = ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF
            page.update()

        # Función para manejar el cambio de caracteres restantes para la contraseña
        def on_password_change(e):
            remaining_chars_text.value = f"Caracteres restantes: {max_password_length - len(nueva_password_field.value)}"
            page.update()

        # Función para manejar el cambio de caracteres restantes para el PIN
        def on_pin_change(e):
            remaining_pin_text.value = f"Caracteres restantes: {max_pin_length - len(pin_text_field.value)}"
            page.update()

        # Función para obtener los datos del cliente usando el PIN
        def on_obtener_datos_click(e):
            if not pin_text_field.value or len(pin_text_field.value) != max_pin_length:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor, ingrese un PIN válido de 4 dígitos."),
                    action="Cerrar"
                )
                page.snack_bar.open = True
            else:
                # Buscar datos del cliente con el PIN ingresado
                cliente = gestor.obtener_cliente_por_pin(int(pin_text_field.value))  # Convertir PIN a entero
                if cliente:
                    nombre_text_field.value = cliente["nombre"]
                    apellido_text_field.value = cliente["apellido"]
                    user_text_field.value = cliente["user_cli"]
                    nueva_password_field.disabled = False
                    confirmar_password_field.disabled = False
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Datos obtenidos correctamente."),
                        action="Cerrar"
                    )
                    page.snack_bar.open = True
                else:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("No se encontró un cliente con ese PIN."),
                        action="Cerrar"
                    )
                    page.snack_bar.open = True

                page.update()

        # Función para manejar el clic en "Actualizar Contraseña"
        def on_actualizar_contrasena_click(e):
            if nueva_password_field.value != confirmar_password_field.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Las contraseñas no coinciden. Intente nuevamente."),
                    action="Cerrar"
                )
                page.snack_bar.open = True
            elif not nueva_password_field.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("La nueva contraseña no puede estar vacía."),
                    action="Cerrar"
                )
                page.snack_bar.open = True
            else:
                # Aquí podrías llamar a un método para actualizar la contraseña en la base de datos
                resultado = gestor.cambiar_contrasena(int(pin_text_field.value), nueva_password_field.value)
                if resultado["status"] == "success":
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Contraseña actualizada exitosamente."),
                        action="Cerrar"
                    )
                    page.snack_bar.open = True
                else:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Hubo un problema al actualizar la contraseña. Intente nuevamente."),
                        action="Cerrar"
                    )
                    page.snack_bar.open = True

                page.update()

        # Crear los campos de texto
        pin_text_field = ft.TextField(
            label="Ingrese su PIN", hint_text="4 dígitos", width=280,
            max_length=max_pin_length, prefix_icon=ft.icons.LOCK, on_change=on_pin_change
        )

        nombre_text_field = ft.TextField(
            label="Nombre", hint_text="", width=280,
            prefix_icon=ft.icons.PERSON, disabled=True
        )

        apellido_text_field = ft.TextField(
            label="Apellido", hint_text="", width=280,
            prefix_icon=ft.icons.PERSON, disabled=True
        )

        user_text_field = ft.TextField(
            label="Usuario", hint_text="", width=280,
            prefix_icon=ft.icons.PERSON, disabled=True
        )

        nueva_password_field = ft.TextField(
            label="Nueva contraseña", hint_text="Ingrese nueva contraseña", width=240,
            prefix_icon=ft.icons.LOCK, password=not password_visible,
            max_length=max_password_length, disabled=True, on_change=on_password_change
        )

        confirmar_password_field = ft.TextField(
            label="Confirmar nueva contraseña", hint_text="Repita la nueva contraseña", width=240,
            prefix_icon=ft.icons.LOCK, password=not password_visible,
            max_length=max_password_length, disabled=True, on_change=on_password_change
        )

        toggle_button = ft.IconButton(
            icon=ft.icons.HIGHLIGHT if not password_visible else ft.icons.HIGHLIGHT_OFF,
            on_click=toggle_password_visibility
        )

        remaining_chars_text = ft.Text(f"Caracteres restantes: {max_password_length}", size=12, color=ft.colors.BLACK)

        # Nuevo texto para mostrar caracteres restantes del PIN
        remaining_pin_text = ft.Text(f"Caracteres restantes: {max_pin_length}", size=12, color=ft.colors.BLACK)

        # Contenedor con todo, ahora incluyendo el nuevo botón
        return ft.Container(
            ft.Column([
                ft.Text("Reestablecer de contraseña", size=30, text_align="center", weight="900", width=280,
                        font_family="Helvetica"),
                pin_text_field,
                remaining_pin_text,  # Mostrar los caracteres restantes del PIN debajo del campo PIN
                ft.ElevatedButton(text="Obtener datos", width=280, bgcolor="black", on_click=on_obtener_datos_click),

                # Campos bloqueados
                nombre_text_field,
                apellido_text_field,
                user_text_field,

                # Campos para la nueva contraseña
                ft.Row([
                    nueva_password_field, toggle_button,
                ], alignment=ft.MainAxisAlignment.START),
                confirmar_password_field,

                # Muestra de caracteres restantes de la contraseña
                remaining_chars_text,

                ft.ElevatedButton(text="Actualizar Contraseña", width=280, bgcolor="black",
                                  on_click=on_actualizar_contrasena_click),

                ft.ElevatedButton(text="Volver a Login", width=280, bgcolor="black", data="ventana1",
                                  on_click=cambiar_ventana)

            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            border_radius=20, width=320, height=680,
            gradient=ft.LinearGradient([ft.colors.PURPLE, ft.colors.BLUE, ft.colors.PURPLE]),
            padding=ft.padding.only(20)
        )

    # VENTANA DE ARTISTA
    def ventanaArtista():
        global ventana_anterior
        ventana_anterior = 4
        print(f"Estado previo: {ventana_anterior}")

        # Verificamos si el valor de 'control' está presente en la sesión, de lo contrario, asignamos un valor por defecto
        control = page.session.get("control") if page.session.get("control") is not None else None

        user = page.session.get("usuario")
        tipo = "artista"
        page.session.set("user", user)
        page.session.set("tipo", tipo)

        componentes.establecer_dimensiones()
        contenedor_buscar = crearBusqueda()

        def actualizar_contenido(e):
            nonlocal control
            control = 2  # Cambiar el valor a 2 para mostrar todos los pedidos
            page.session.set("control", control)  # Guardar el valor de control en la sesión correctamente
            e.control.data = "ventana4"  # Asignamos directamente "ventana4" al control
            cambiar_ventana(e)  # Esto actualizará la vista a la ventana correspondiente
            page.update()  # Actualizamos la pantalla para reflejar el cambio

        def reestablecer_contenido(e):
            nonlocal control
            control = None  # Cambiar el valor a None para mostrar los últimos 10 pedidos
            page.session.set("control", control)  # Guardar el valor de control en la sesión correctamente
            e.control.data = "ventana4"  # Asignamos directamente "ventana4" al control
            cambiar_ventana(e)  # Esto actualizará la vista a la ventana correspondiente
            page.update()  # Actualizamos la pantalla para reflejar el cambio

        def ver_sin_precio(e):
            nonlocal control
            control = 3  # Cambiar el valor a 3 para mostrar los pedidos sin precio
            page.session.set("control", control)  # Guardar el valor de control en la sesión correctamente
            e.control.data = "ventana4"  # Asignamos directamente "ventana4" al control
            cambiar_ventana(e)  # Esto actualizará la vista a la ventana correspondiente
            page.update()  # Actualizamos la página para reflejar el cambio

        listaPedidos = last10_view(user, tipo)
        listaPedidosT = mostrar_pedidos_en_listview(user, tipo)
        listaPedidosSinPrecio = mostrar_pedidos_sin_precio(user, tipo)

        # Actualizamos la lista según el valor de control
        if control is None:
            lista_mostrar = listaPedidos  # Mostrar la lista de pedidos original
        elif control == 2:
            lista_mostrar = listaPedidosT  # Mostrar la lista de pedidos alterna
        else:
            lista_mostrar = listaPedidosSinPrecio  # Caso en que control es 3 (pedidos sin precio), puedes poner la lista vacía o algo específico

        contenedor1 = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Listado de Pedidos", size=24, weight="bold", color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER, width=1200),

                    # Ajuste de la lista para que no ocupe todo el espacio
                    ft.Container(
                        content=lista_mostrar,
                        height=450,  # Ajusta el tamaño de la lista para que deje espacio para los botones
                        expand=True,
                    ),

                    # Fila con los botones "Ver todo" y "Ver pedidos sin precio"
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Ver todos los pedidos",  # Texto del botón
                                on_click=actualizar_contenido,
                                width=110,  # Ancho del botón
                            ),
                            ft.ElevatedButton(
                                "Ver últimos 10 pedidos",  # Texto del botón
                                on_click=reestablecer_contenido,
                                width=110,  # Ancho del botón
                            ),
                            ft.ElevatedButton(
                                "Ver pedidos sin precio",  # Texto del botón
                                on_click=ver_sin_precio,  # Función que manejará la acción
                                width=110,  # Ancho del botón
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centra la fila de botones
                        spacing=20,  # Espaciado entre los botones
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            width=500,
            height=620,
            border_radius=10,
            padding=20,
            expand=True,
            gradient=ft.LinearGradient([ft.colors.PURPLE, ft.colors.BLUE, ft.colors.PURPLE]),
        )

        # Contenedor 2 para calcular totales
        filas_materiales, resultados = [], []

        def calcular_totales(e):
            total = 0
            for fila, resultado in zip(filas_materiales, resultados):
                try:
                    cantidad = float(fila.controls[1].value or 0)
                    costo_unitario = float(fila.controls[2].value or 0)
                    subtotal = cantidad * costo_unitario
                    resultado.value = f"Subtotal: {subtotal:.2f}"
                    total += subtotal
                except ValueError:
                    resultado.value = "Subtotal: 0.00"
            total_campo.value = f"{total:.2f}"
            page.update()

        def limpiar_campos(e=None):
            """Función para limpiar los campos del formulario."""
            for fila in filas_materiales:
                fila.controls[0].value = None  # Limpiar el dropdown
                fila.controls[1].value = ""  # Limpiar el campo de cantidad
                fila.controls[2].value = ""  # Limpiar el campo de costo unitario
            for resultado in resultados:
                resultado.value = "Subtotal: 0.00"
            total_campo.value = "0.00"
            page.update()

        materiales = [f"Material {chr(65 + i)}" for i in range(10)]
        for i in range(3):
            fila = ft.Row(
                controls=[
                    ft.Dropdown(options=[ft.dropdown.Option(m) for m in materiales], hint_text=f"Material {i + 1}",
                                width=200),
                    ft.TextField(hint_text="Cantidad", width=100, on_change=calcular_totales),
                    ft.TextField(hint_text="C/U", width=100, on_change=calcular_totales),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            resultado = ft.Text(value="Subtotal: 0.00", color=ft.colors.WHITE)
            filas_materiales.append(fila)
            resultados.append(resultado)

        total_label, total_campo = ft.Text(value="Importe total:", size=16, color=ft.colors.WHITE), ft.TextField(
            value="0.00", read_only=True, width=100, text_align=ft.TextAlign.RIGHT)

        def enviar_factura(e):
            #global selected_pedido  # Asegúrate de que estás utilizando la variable global

            # Verificar que todos los campos estén completos
            for fila in filas_materiales:
                if not fila.controls[0].value or not fila.controls[1].value or not fila.controls[2].value:
                    page.snack_bar = ft.SnackBar(ft.Text("Por favor, complete todos los campos."), open=True)
                    page.update()
                    return

            # Verificar si se ha seleccionado un pedido
            if selected_pedido is None:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Por favor, seleccione el pedido al cual se le asignará el precio."), open=True)
                page.update()
                return

            try:
                total = float(total_campo.value)  # Asegurarnos de que el valor sea un número
                # Actualizar el precio directamente en la base de datos
                print(f"Pedido seleccionado: {selected_pedido}, Total: {total}")  # Debugging
                gestor.actualizar_precio_pedido(selected_pedido, total)
                tipo='artista'

                # Opcional: Refrescar la lista de pedidos después de actualizar el precio
                pedidos_actualizados = gestor.obtener_pedidos_db('',tipo)  # Obtenemos la lista de pedidos actualizada
                contenedor1.content.controls[1] = last10_view('',tipo)  # Actualiza la lista de pedidos
                page.snack_bar = ft.SnackBar(ft.Text("Factura enviada y lista actualizada."), open=True)

                # Limpiar campos automáticamente después de enviar la factura
                limpiar_campos()
                page.update()

            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("El precio debe ser un número válido."), open=True)
                page.update()

        contenedor2 = ft.Container(
            content=ft.Column(
                controls=[
                    # Contenedor para el título, centrado dentro del Row
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Detalles del Pedido", size=24, weight="bold", color=ft.colors.WHITE,
                                text_align=ft.TextAlign.CENTER,  # Alineación del texto
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Alineación del Row en el centro
                    ),

                    # Espaciado adicional entre el título y los campos
                    ft.Container(height=30),  # Aquí ajustas la separación entre el título y los campos

                    # Columnas con resultados y filas de materiales
                    ft.Column(
                        controls=[
                            ft.Column([resultado, fila], spacing=5)
                            for resultado, fila in zip(resultados, filas_materiales)
                        ],
                        spacing=15,
                        expand = True
                    ),

                    # Separación entre la sección de campos y el total
                    ft.Row(
                        controls=[total_label, total_campo],
                        alignment=ft.MainAxisAlignment.CENTER, spacing=20
                    ),

                    # Más espacio antes del botón
                    ft.Container(height=20),  # Agregar más separación entre subtotal y el botón

                    # Fila con botones centrados
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Enviar factura a cliente", on_click=enviar_factura, bgcolor=ft.colors.GREEN_500,
                                color=ft.colors.WHITE
                            ),
                            ft.ElevatedButton(
                                text="Limpiar", on_click=limpiar_campos, bgcolor=ft.colors.RED_500,
                                color=ft.colors.WHITE
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,  # Alineación vertical de los controles
                spacing=30,  # Espaciado general entre los controles
                expand = True
            ),
            border_radius=10, padding=20, expand=True,
            gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE, ft.colors.RED]),
        )

        main_section = ft.Row(controls=[contenedor1, contenedor2], alignment=ft.MainAxisAlignment.CENTER, spacing=10,
                              expand=True)
        layout = ft.Column(controls=[contenedor_buscar, main_section], alignment=ft.MainAxisAlignment.CENTER,
                           expand=True)

        return layout

        # VENTANA DE CLIENTE

    def ventanaCliente():
        global ventana_anterior
        ventana_anterior = 5
        print(f"Estado previo: {ventana_anterior}")
        # Verificamos si el valor de 'control' está presente en la sesión, de lo contrario, asignamos un valor por defecto
        control = page.session.get("control") if page.session.get("control") is not None else None
        user= page.session.get("usuario")
        tipo="cliente"
        page.session.set("user", user)
        page.session.set("tipo", tipo)
        contenedor_buscar = crearBusqueda()
        componentes.establecer_dimensiones()
        tamano_pintura, estilo_pintura, tonalidades, material_pintura, tipo_pintura = ft.Ref[ft.Dropdown](), ft.Ref[
            ft.Dropdown](), ft.Ref[
            ft.Dropdown](), ft.Ref[ft.Dropdown](), ft.Ref[ft.Dropdown]()

        def actualizar_contenido(e):
            nonlocal control
            control = 2  # Cambiar el valor a 2 para mostrar todos los pedidos
            page.session.set("control", control)  # Guardar el valor de control en la sesión correctamente
            e.control.data = "ventana5"  # Asignamos directamente "ventana4" al control
            cambiar_ventana(e)  # Esto actualizará la vista a la ventana correspondiente
            page.update()  # Actualizamos la pantalla para reflejar el cambio

        def reestablecer_contenido(e):
            nonlocal control
            control = None  # Cambiar el valor a None para mostrar los últimos 10 pedidos
            page.session.set("control", control)  # Guardar el valor de control en la sesión correctamente
            e.control.data = "ventana5"  # Asignamos directamente "ventana4" al control
            cambiar_ventana(e)  # Esto actualizará la vista a la ventana correspondiente
            page.update()  # Actualizamos la pantalla para reflejar el cambio

        def ver_sin_precio(e):
            nonlocal control
            control = 3  # Cambiar el valor a 3 para mostrar los pedidos sin precio
            page.session.set("control", control)  # Guardar el valor de control en la sesión correctamente
            e.control.data = "ventana5"  # Asignamos directamente "ventana4" al control
            cambiar_ventana(e)  # Esto actualizará la vista a la ventana correspondiente
            page.update()  # Actualizamos la página para reflejar el cambio

        listaPedidos = last10_view(user,tipo)
        listaPedidosT = mostrar_pedidos_en_listview(user,tipo)
        listaPedidosSinPrecio = mostrar_pedidos_sin_precio(user,tipo)

        # Actualizamos la lista según el valor de control
        if control is None:
            lista_mostrar = listaPedidos  # Mostrar la lista de pedidos original
        elif control == 2:
            lista_mostrar = listaPedidosT  # Mostrar la lista de pedidos alterna
        else:
            lista_mostrar = listaPedidosSinPrecio  # Caso en que control es 3 (pedidos sin precio), puedes poner la lista vacía o algo específico

        def limpiar_campos(e):
            # Limpiar los valores de los Dropdowns
            tamano_pintura.current.value = None
            estilo_pintura.current.value = None
            tonalidades.current.value = None
            material_pintura.current.value = None
            tipo_pintura.current.value = None

            # Actualizar la página para reflejar los cambios
            page.update()

        def guardar_datos(e):
            # Obtener valores de los Dropdowns
            tamano, estilo, tonos, material, tipo = (
                tamano_pintura.current.value, estilo_pintura.current.value, tonalidades.current.value,
                material_pintura.current.value,
                tipo_pintura.current.value)

            # Verificar si los valores están vacíos
            if not tamano or not estilo or not tonos or not material or not tipo:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos."), open=True)
                page.update()
                return

            # Asignar un valor por defecto de 0.00 para el precio (aún no se especifica)
        
            precio = 0.00
            
            try:
            # Crear una instancia de Pedido con los datos del formulario
                pedido = Pedido(
                    id=None,
                    tamano=tamano,
                    estilo=estilo,
                    tonalidades=tonos,
                    material=material,
                    tipo=tipo,
                    precio=precio,  # El precio por defecto es 0.00
                    nombre_cliente=nombreA,  # Asumiendo que el "user" es el nombre del cliente
                    apellido_cliente=apellidoA,  # Asumiendo que tienes la variable "apellidoA"
                    user_cliente = user,
                    id_cli=None  # Este puede ser el ID del cliente si tienes acceso a él (o None si es autoincrementable)
                )
                
                print(pedido.tamano, pedido.estilo, pedido.tonalidades, pedido.material, pedido.tipo, user, pedido.nombre_cliente, pedido.apellido_cliente)

            # Llamar a guardar_pedido_db con los atributos de la instancia de Pedido
                gestor.guardar_pedido_db(pedido.tamano, pedido.estilo, pedido.tonalidades, pedido.material, pedido.tipo, user, pedido.nombre_cliente, 
                                         pedido.apellido_cliente, pedido.user_cliente)

            # Mostrar mensaje de éxito
                page.snack_bar = ft.SnackBar(ft.Text("Pedido guardado correctamente."), open=True)

            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar el pedido: {str(e)}"), open=True)
    
            # Limpiar la pantalla
            page.controls.clear()

            # Volver a llamar a la ventana 5
            page.controls.append(ventanaCliente())

            # Actualizar la página para reflejar los cambios
            page.update()

            # Mostrar el SnackBar
            page.snack_bar.open = True
            page.update()

        contenedor2 = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Agregar Pedido", size=24, weight="bold", color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER, width=1000),
                    ft.Container(height=10),  # Espacio aumentado entre el título y los campos
                    ft.Column(controls=[
                        ft.Row(controls=[
                            ft.Text(label, size=16, weight="bold", color=ft.colors.WHITE, width=200),
                            ft.Dropdown(ref=ref, options=[ft.dropdown.Option(opt) for opt in options], width=250)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                        for label, ref, options in [
                            ("Tamaño:", tamano_pintura, ["Muy grande", "Grande", "Mediano", "Pequeño", "Retrato"]),
                            ("Estilo:", estilo_pintura,
                             ["Moderno", "Clásico", "Retro", "Realismo", "Impresionismo", "Expresionismo", "Cubismo",
                              "Abstracto", "Pop Art",
                              "Barroco", "Renacentista", "Futurista", "Minimalista"]),
                            ("Tonalidades:", tonalidades,
                             ["Cálidos", "Fríos", "Oscuros", "Neutras", "Saturadas", "Desaturadas", "Alegres",
                              "Meláncolicas", "Serenas",
                              "Sólidas", "Terrosas", "Marinas"]),
                            ("Material:", material_pintura, ["Madera", "Metal", "Pintura", "Digital", "Retrato"]),
                            (
                                "Tipo:", tipo_pintura,
                                ["Acuarela", "Óleo", "Acrílico", "Aerosol", "Rodillos", "Pinceles"]),
                        ]
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                    ft.Row(controls=[
                        ft.ElevatedButton(text="Agregar", on_click=guardar_datos, bgcolor=ft.colors.BLUE_700,
                                          color=ft.colors.WHITE),
                        ft.ElevatedButton(text="Limpiar", on_click=limpiar_campos, bgcolor=ft.colors.RED_700,   #limpiar_campos, bgcolor=ft.colors.RED_700,
                                          color=ft.colors.WHITE)  # Botón de limpiar
                    ], alignment=ft.MainAxisAlignment.CENTER, expand=False)
                ], spacing=20, alignment=ft.MainAxisAlignment.CENTER
            ),
            border_radius=10, padding=20, expand=True,
            gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE, ft.colors.RED]),  # Aplicar gradiente
            width=800,  # Establecer el ancho
            height=600  # Establecer la altura
        )

        page.update()  # Actualizar pantalla con el pedido

        # ListView que muestra los pedidos
        contenedor_listado = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Pedidos", text_align="center", size=24, weight="bold", color=ft.colors.WHITE, width=680),
                    # Ajuste de la lista para que no ocupe todo el espacio
                    ft.Container(
                        content=lista_mostrar,
                        height=450,  # Ajusta el tamaño de la lista para que deje espacio para los botones
                        expand=True,
                    ),
                    ft.Row(
                        controls = [
                            ft.ElevatedButton(
                                "Ver todos los pedidos",  # Texto del botón
                                on_click=actualizar_contenido,
                                width=110,  # Ancho del botón
                            ),
                            ft.ElevatedButton(
                                "Ver últimos 10 pedidos",  # Texto del botón
                                on_click=reestablecer_contenido,
                                width=110,  # Ancho del botón
                            ),
                            ft.ElevatedButton(
                                "Ver pedidos sin precio",  # Texto del botón
                                on_click=ver_sin_precio,  # Función que manejará la acción
                                width=110,  # Ancho del botón
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER,  # Centra la fila de botones
                        spacing=20,  # Espaciado entre los botones
                    )
                ],
                alignment=ft.MainAxisAlignment.START, spacing=20,
            ),
            width=500, height=600, border_radius=10, padding=20, expand=True,
            gradient=ft.LinearGradient([ft.colors.PURPLE, ft.colors.BLUE, ft.colors.PURPLE]),
        )
        page.update()  # Actualizar pantalla con el listado de pedidos

        layout = ft.Column(controls=[contenedor_buscar,
                                     ft.Row(controls=[contenedor_listado, contenedor2],
                                            alignment=ft.MainAxisAlignment.CENTER, spacing=10)],
                           alignment=ft.MainAxisAlignment.CENTER, expand=True
                           )

        return layout

    # VENTANA DE BUSQUEDA

    def ventanaConsultas():
        usuario = page.session.get("user")
        tipo = page.session.get("tipo")

        componentes.establecer_dimensiones()
        contenedor_buscar = crearBusqueda()

        global estado_ventana  # Asegúrate de usar la variable global

        # Ícono condicional
        icono_condicional = ft.IconButton(
            icon=ft.icons.PERSON,
            icon_size=30,
            data="ventana5" if ventana_anterior == 5 else "ventana4",
            on_click=cambiar_ventana,
            icon_color=ft.colors.WHITE,
        )

        # Configuración del ancho uniforme para los campos
        campo_width = 305  # Ajustar al tamaño deseado

        # Componentes de la interfaz
        tamano_dropdown = ft.Dropdown(
            label="Tamaño",
            options=[ft.dropdown.Option("Muy grande"), ft.dropdown.Option("Grande"), ft.dropdown.Option("Mediano"),
                     ft.dropdown.Option("Pequeño"), ft.dropdown.Option("Retrato")],
            width=campo_width
        )

        estilo_dropdown = ft.Dropdown(
            label="Estilo",
            options=[ft.dropdown.Option("Moderno"), ft.dropdown.Option("Clásico"), ft.dropdown.Option("Retro"),
                     ft.dropdown.Option("Realismo"), ft.dropdown.Option("Impresionismo"),
                     ft.dropdown.Option("Expresionismo"),
                     ft.dropdown.Option("Cubismo"), ft.dropdown.Option("Abstracto"), ft.dropdown.Option("Pop Art"),
                     ft.dropdown.Option("Barroco"), ft.dropdown.Option("Renacentista"), ft.dropdown.Option("Futurista"),
                     ft.dropdown.Option("Minimalista")],
            width=campo_width
        )

        tonalidades_dropdown = ft.Dropdown(
            label="Tonalidades",
            options=[ft.dropdown.Option("Cálidos"), ft.dropdown.Option("Fríos"), ft.dropdown.Option("Oscuros"),
                     ft.dropdown.Option("Neutras"), ft.dropdown.Option("Saturadas"), ft.dropdown.Option("Desaturadas"),
                     ft.dropdown.Option("Alegres"), ft.dropdown.Option("Meláncolicas"), ft.dropdown.Option("Serenas"),
                     ft.dropdown.Option("Sólidas"), ft.dropdown.Option("Terrosas"), ft.dropdown.Option("Marinas")],
            width=campo_width
        )

        material_dropdown = ft.Dropdown(
            label="Material",
            options=[ft.dropdown.Option("Madera"), ft.dropdown.Option("Metal"), ft.dropdown.Option("Pintura"),
                     ft.dropdown.Option("Digital"), ft.dropdown.Option("Retrato")],
            width=campo_width
        )

        tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[ft.dropdown.Option("Acuarela"), ft.dropdown.Option("Óleo"), ft.dropdown.Option("Acrílico"),
                     ft.dropdown.Option("Aerosol"), ft.dropdown.Option("Rodillos"), ft.dropdown.Option("Pinceles")],
            width=campo_width
        )

        id_input = ft.TextField(label="ID del pedido (si lo tienes)", width=campo_width)

        resultados_area = ft.Column(expand=True)

        # Inicializamos la sección de resultados con un contenedor vacío
        contenedor_resultados = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "No se han realizado búsquedas aún.",
                            weight=ft.FontWeight.BOLD,
                            size=20,
                            color=ft.colors.WHITE
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrado en el eje Y
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centrado en el eje X
                ),
                height=586,
                width=800,
                gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE, ft.colors.RED]),
                border_radius=20,
                expand=True
            )

        resultados_area.controls.append(contenedor_resultados)

        def mostrar_resultados(pedidos):
            # Crear un ListView limpio
            list_view = ft.ListView(expand=True, spacing=10, padding=20)

            if pedidos:  # Asegurarse de que hay pedidos
                for pedido in pedidos:
                    try:
                        # Verificar que el pedido tenga al menos 10 elementos
                        if len(pedido) >= 10:
                            pedido_id, tamano, estilo, tonalidades, material, tipo, precio, nombre_cliente, apellido_cliente, user_cliente = pedido

                            # Crear y agregar un ListTile al ListView
                            list_view.controls.append(
                                ft.ListTile(
                                    title=ft.Text(f"Pedido #{pedido_id}: {tamano} - {estilo}"),
                                    subtitle=ft.Text(
                                        f"Tonalidades: {tonalidades} | Material: {material} | Tipo: {tipo}\n| Precio: ${precio:.2f} | Cliente: {nombre_cliente} {apellido_cliente} | Usuario: {user_cliente}"

                                    ),
                                    trailing=ft.Icon(
                                        ft.Icons.CHECK_CIRCLE if precio else ft.Icons.PENDING,
                                        color=ft.Colors.GREEN if precio else ft.Colors.RED,
                                    ),
                                    on_click=lambda e, pedido_id=pedido_id: seleccionar_pedido(pedido_id),
                                )
                            )
                        else:
                            # Agregar mensaje de error para datos incompletos
                            list_view.controls.append(
                                ft.ListTile(
                                    title=ft.Text("Pedido inválido", color=ft.colors.RED),
                                    subtitle=ft.Text(f"Datos incompletos: {pedido}"),
                                )
                            )
                    except Exception as e:
                        # Agregar mensaje de error para cualquier excepción
                        list_view.controls.append(
                            ft.ListTile(
                                title=ft.Text("Error procesando pedido", color=ft.colors.RED),
                                width = 200,
                                subtitle=ft.Text(str(e)),
                            )
                        )
            else:
                # Si no hay pedidos, mostrar un mensaje
                list_view.controls.append(
                    ft.ListTile(
                        title=ft.Text(
                            "No se encontraron pedidos con los criterios especificados.",
                            width = 200,
                            weight=ft.FontWeight.BOLD,
                            size=20,
                            color=ft.colors.RED_ACCENT_200,
                        )
                    )
                )

            # Actualizar el contenido del contenedor principal de resultados
            contenedor_resultados.content = list_view
            contenedor_resultados.update()  # Asegurarse de que el contenedor se refresca
            resultados_area.update()  # Asegurar que el área completa se actualice

            # Log para depuración
            print("Pedidos procesados:", pedidos)

        def buscar_pedidos(tipo, user, nombre, apellido, id):
            criterios = {}

            # Verificar si los filtros tienen valores
            if tamano_dropdown.value:
                criterios['tamano'] = tamano_dropdown.value
            if estilo_dropdown.value:
                criterios['estilo'] = estilo_dropdown.value
            if tonalidades_dropdown.value:
                criterios['tonalidades'] = tonalidades_dropdown.value
            if material_dropdown.value:
                criterios['material'] = material_dropdown.value
            if tipo_dropdown.value:
                criterios['tipo'] = tipo_dropdown.value

            # Verificar si alguno de los campos de texto tiene un valor
            if nombre_input.value:
                criterios['nombreCliente'] = nombre_input.value
            if apellido_input.value:
                criterios['apellidoCliente'] = apellido_input.value
            if id_input.value:
                criterios['id'] = id_input.value

            # Verificar si se han ingresado criterios para la búsqueda
            if not criterios:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor, complete al menos un campo de búsqueda."),
                    action="Cerrar"
                )
                page.snack_bar.open = True
                page.update()
                return  # Salir de la función si no hay criterios

            # Asumimos que gestor.buscar_general devuelve los pedidos que cumplen con los criterios
            pedidos = gestor.buscar_general(criterios, tipo, user, nombre, apellido, id)

            # Verificar si se encontraron pedidos
            if not pedidos:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("No se encontraron pedidos con los criterios especificados."),
                    action="Cerrar"
                )
                page.snack_bar.open = True
                page.update()

            mostrar_resultados(pedidos)

        def limpiar_campos(e):
            # Limpiar valores de los campos de texto
            id_input.value = ""
            id_input.update()

            # Limpiar los dropdowns y demás entradas
            dropdowns = [
                tamano_dropdown, estilo_dropdown, tonalidades_dropdown,
                material_dropdown, tipo_dropdown, nombre_input, apellido_input
            ]

            for dropdown in dropdowns:
                dropdown.value = None  # Vaciamos los valores de los dropdowns

            # Limpiar la sección de resultados
            contenedor_resultados.content = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "No se han realizado búsquedas aún.",
                            weight=ft.FontWeight.BOLD,
                            size=20,
                            color=ft.colors.WHITE
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                height=586,
                width=800,
                gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE, ft.colors.RED]),
                border_radius=20,
                expand=True
            )

            # Añadir los controles a la página si es necesario antes de actualizar
            if not page.controls:
                page.add(tamano_dropdown, estilo_dropdown, tonalidades_dropdown, material_dropdown, tipo_dropdown,
                         id_input)

            # Actualizar después de asegurarse que los controles están en la página
            contenedor_resultados.update()
            resultados_area.update()

            # Si los campos están vacíos, asegurarse de actualizar los dropdowns
            for dropdown in dropdowns:
                dropdown.update()  # Solo actualizar los dropdowns después de vaciarlos

        def verTodo_button_click(e):
            # Obtener todos los pedidos y actualizar la vista
            listaPedidos = mostrar_pedidos_en_listview(usuario, tipo)
            contenedor_resultados.content = listaPedidos  # Actualiza el contenido del contenedor
            resultados_area.update()  # Actualizar la interfaz

        buscar_button = ft.ElevatedButton(
            "Buscar", on_click=lambda e: buscar_pedidos(tipo, usuario, nombre_input.value, apellido_input.value,
                                                        id_input.value), width=80
        )
        limpiar_button = ft.ElevatedButton("Limpiar", on_click=limpiar_campos, width=80)

        # Determinar el comportamiento del botón en función de estado_ventana
        verTodo_button = ft.ElevatedButton("Ver Todo", on_click=verTodo_button_click, width=80)

        nombre_input = ft.TextField(label="Nombre", width=campo_width)
        apellido_input = ft.TextField(label="Apellido", width=campo_width)

        controles_busqueda = [ft.Text("Filtrar por", weight=ft.FontWeight.BOLD)]

        if ventana_anterior == 4:
            controles_busqueda.extend([nombre_input, apellido_input])

        controles_busqueda.extend([
            tamano_dropdown,
            estilo_dropdown,
            tonalidades_dropdown,
            material_dropdown,
            tipo_dropdown,
            id_input,
            ft.Container(height=10),
            ft.Row(
                controls=[buscar_button, limpiar_button, verTodo_button],
                alignment=ft.MainAxisAlignment.START,
                spacing=33,
            )
        ])

        padding_valor = 20 if ventana_anterior == 4 else 60

        # Usamos Row para centrar los campos
        campos_busqueda = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=controles_busqueda,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
            border_radius=20,
            padding=padding_valor,
            width=450,
            gradient=ft.LinearGradient([ft.colors.PURPLE, ft.colors.BLUE, ft.colors.PURPLE]),
        )

        contenedor_botones = ft.Container(
            content=ft.Row(
                controls=[
                    icono_condicional,
                    ft.IconButton(ft.icons.LOGOUT, icon_size=30, data="ventana1", on_click=cambiar_ventana,
                                  icon_color=ft.colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            border_radius=20,
            margin=10,
            padding=10,
            gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE_700, ft.colors.BLUE_700]),
        )

        layout = ft.Column(
            controls=[
                contenedor_botones,
                ft.Row(controls=[campos_busqueda, resultados_area], expand=True)
            ],
            expand=True
        )

        return layout

    def ventanaResumen():
        contenedor_buscar = crearBusqueda()
        componentes.establecer_dimensiones()

        # Obtener el resumen de datos (cantidad de clientes y pedidos)
        cantidad_clientes, cantidad_pedidos, totalEnCuenta = gestor.obtener_resumen_datos()

        # Obtener el top 10 clientes con más pedidos
        clientes_top_10 = gestor.obtener_top_10_clientes()

        # Crear la tabla de datos
        table_data = [
            ["Clientes", cantidad_clientes],
            ["Pedidos", cantidad_pedidos],
        ]

        # Definir la estructura de la tabla
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Categoría", size=26, weight="bold", color=ft.colors.BLACK)),  # Texto más grande
                ft.DataColumn(ft.Text("Cantidad", size=26, weight="bold", color=ft.colors.BLACK)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(row[0], size=23, weight="bold", color=ft.colors.BLACK)),
                    ft.DataCell(ft.Text(str(row[1]), size=23, color=ft.colors.BLACK))
                ]) for row in table_data
            ],
            bgcolor=ft.colors.AMBER_ACCENT_700,
            border_radius=10,
            width=400,
            height=300
        )

        # Crear el ListView para mostrar los 10 clientes con más pedidos
        list_view = ft.ListView(
            spacing=10,
            width=400,
            height=300,
        )

        # Si la consulta de clientes con más pedidos fue exitosa, los agregamos al ListView
        if clientes_top_10["status"] == "success":
            for cliente in clientes_top_10["clientes"]:
                list_view.controls.append(ft.Text(cliente, size=18, weight="bold", color=ft.colors.WHITE))
        else:
            list_view.controls.append(
                ft.Text(clientes_top_10["message"], size=18, weight="bold", color=ft.colors.WHITE))

        # Contenedor estilizado para el resumen de datos
        contenedor_resumen = ft.Container(
            content=ft.Column(
                [
                    ft.Text("         Resumen de Datos", size=28, weight="bold", color=ft.colors.WHITE),  # Texto más grande
                    table,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centramos el contenido
                spacing=20
            ),
            bgcolor=ft.colors.INDIGO_500,
            border_radius=15,
            padding=20,
            width=575,
            height=450,
            alignment=ft.alignment.center
        )

        # Contenedor estilizado para los clientes con más pedidos
        contenedor_clientes = ft.Container(
            content=ft.Column(
                [
                    ft.Text("     Clientes con Más Pedidos", size=28, weight="bold", color=ft.colors.WHITE),
                    # Título ajustado
                    list_view
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20
            ),
            bgcolor=ft.colors.DEEP_ORANGE_500,
            border_radius=15,
            padding=20,
            width=575,
            height=450,
            alignment=ft.alignment.center
        )

        # Contenedor estilizado para mostrar el total en cuenta
        contenedor_cuenta = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        name=ft.icons.ATTACH_MONEY,
                        size=60,  # Icono más grande
                        color=ft.colors.GREEN_ACCENT_400
                    ),
                    ft.Text(
                        f"Total en Cuenta: ${totalEnCuenta:.2f}",
                        size=32,  # Texto más grande
                        weight="bold",
                        color=ft.colors.WHITE
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            bgcolor=ft.colors.GREEN_900,
            border_radius=20,
            padding=30,
            width=1200,  # Más ancho para llenar la pantalla
            height=120,
            alignment=ft.alignment.center
        )

        # Crear la página con tabla, ListView y total debajo
        page.add(
            ft.Column(
                [
                    contenedor_buscar,
                    ft.Row(
                        controls=[contenedor_resumen, contenedor_clientes],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        spacing=30
                    ),
                    #ft.Container(height=-5),  # Espaciado entre filas
                    contenedor_cuenta
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )

        # Actualizar la página
        page.update()

    # Configuración inicial: Mostrar la Ventana 1
    page.bgcolor = ft.colors.GREY_900  # Fondo gris intermedio
    page.controls.append(ventanaLogin())
    page.window_resizable = False  # Opcional: Desactiva el redimensionamiento de la ventana
    page.window_maximizable = False  # Opcional: Desactiva la maximización de la ventana
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Centra verticalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centra horizontalmente
    page.update()

ft.app(target=main)

