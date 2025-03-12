import sqlite3
import os
import re
from Clases_Y_Componentes import *


# CLASE QUE PERMITE EL MANEJO Y FLUJO DE LA BASE DE DATOS
class GestorPedidos:
    def __init__(self, db_name="pedidos.db"):
        self.db_name = db_name

    def init_db(self):
        """Inicializa la base de datos y crea las tablas necesarias."""
        conn = None  # Aseguramos que `conn` se inicializa fuera del bloque try
        try:
            # Verificar si la base de datos existe, y si no, crearla
            if not os.path.exists(self.db_name):
                print("La base de datos no existe. Se creará nuevamente.")
            else:
                print("La base de datos existe. Asegurando que las tablas estén actualizadas.")

            # Conexión a la base de datos (si no existe, SQLite la creará automáticamente)
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Crear la tabla 'clientes'
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS clientes (
                       id_cli INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_cli TEXT NOT NULL UNIQUE,
                       pass_cli TEXT NOT NULL,
                       nombre TEXT NOT NULL,
                       apellido TEXT NOT NULL,
                       pin INTEGER NOT NULL UNIQUE,
                       cantidadPedidos INTEGER DEFAULT 0
                   )
               ''')

            # Crear la tabla 'pedidos'
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS pedidos (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tamano TEXT,
                       estilo TEXT,
                       tonalidades TEXT,
                       material TEXT,
                       tipo TEXT,
                       precio REAL DEFAULT 0.00,
                       nombreCliente TEXT NOT NULL,
                       apellidoCliente TEXT NOT NULL,
                       userCliente TEXT NOT NULL,
                       id_cli INTEGER,
                       FOREIGN KEY(id_cli) REFERENCES clientes(id_cli)
                   )
               ''')

            # Crear la tabla 'artista'
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artista (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_artista TEXT NOT NULL UNIQUE,
                    pass_artista TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    totalEnCuenta REAL DEFAULT 0.00
                )
            ''')

            # Insertar usuario por defecto en 'artista' si no existe
            cursor.execute("SELECT COUNT(*) FROM artista WHERE user_artista = 'leonardo1234'")
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO artista (user_artista, pass_artista, nombre, apellido, totalEnCuenta)
                    VALUES ('leonardo1234', 'art1234', 'Leonardo', 'Lopez', 0.00)
                ''')
                print("Datos por defecto para el artista 'Leonardo' insertados.")

            # Confirmar la transacción
            conn.commit()
            print("Base de datos inicializada correctamente.")

        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")

        finally:
            if conn:  # Verificamos si `conn` no es None antes de cerrarlo
                conn.close()

    # Metodos de busqueda en la BD

    def buscar_general(self, criterios, tipo, user=None, nom=None, apel=None, id=None):
        """Busca pedidos según criterios específicos."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Construir la consulta base
            query = """
                SELECT p.id, p.tamano, p.estilo, p.tonalidades, p.material, p.tipo, p.precio, 
                       c.nombre, c.apellido, c.user_cli
                FROM pedidos p
                JOIN clientes c ON p.userCliente = c.user_cli
                WHERE
            """
            filtros = []

            # Para tipo "artista"
            if tipo == 'artista':
                if nom:
                    criterios['nombre'] = nom.strip()
                if apel:
                    criterios['apellido'] = apel.strip()
                if id:
                    criterios['id'] = id

                # Añadir filtros según los criterios proporcionados
                filtros = [f"LOWER({campo}) = LOWER(?)" for campo in criterios.keys()]

            # Para tipo "cliente"
            elif tipo == 'cliente':
                # Obtener nombre y apellido del cliente desde la tabla "clientes"
                cursor.execute("SELECT nombre, apellido FROM clientes WHERE user_cli = ?", (user,))
                resultado = cursor.fetchone()

                if resultado:
                    nombre, apellido = resultado
                    # Usar el nombre y apellido del cliente como criterios si no se especifican otros
                    criterios['nombre'] = nombre.strip()
                    criterios['apellido'] = apellido.strip()
                    if id:
                        criterios['id'] = id

                    # Construir los filtros
                    filtros = [f"LOWER({campo}) = LOWER(?)" for campo in criterios.keys()]
                else:
                    print("No se encontró al cliente con el usuario especificado.")
                    return []

            # Si no hay criterios, devolver todos los resultados
            if not filtros:
                query += "1 = 1"  # Condición que siempre es verdadera para evitar errores de sintaxis
            else:
                query += " AND ".join(filtros)

            # Imprimir la consulta para depuración
            print("Consulta SQL:", query)
            print("Valores:", tuple(criterios.values()))

            # Ejecutar la consulta y retornar los resultados
            cursor.execute(query, tuple(criterios.values()))
            resultados = cursor.fetchall()

            if not resultados:
                print("No se encontraron pedidos con los criterios especificados.")
            return resultados

        except sqlite3.Error as e:
            print(f"Error al buscar pedidos: {e}")
            return []
        finally:
            conn.close()


    # Metodos de guardados de la BD

    def guardar_pedido_db(self, tamano, estilo, tonalidades, material, tipo, user, nombreCliente, apellidoCliente,
                          user_cliente):
        """Guarda un pedido en la base de datos y actualiza el número de pedidos del cliente."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Obtener el id_cli del cliente usando su nombre de usuario
            cursor.execute("SELECT id_cli FROM clientes WHERE user_cli = ?", (user,))
            resultado = cursor.fetchone()

            if resultado:
                user_id = resultado[0]

                # Guardar el pedido en la tabla 'pedidos'
                cursor.execute('''
                    INSERT INTO pedidos (tamano, estilo, tonalidades, material, tipo, id_cli, nombreCliente, apellidoCliente, userCliente)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (tamano, estilo, tonalidades, material, tipo, user_id, nombreCliente, apellidoCliente, user))

                # Incrementar el número de pedidos del cliente
                cursor.execute('''
                    UPDATE clientes
                    SET cantidadPedidos = cantidadPedidos + 1
                    WHERE user_cli = ?
                ''', (user,))

                # Confirmar la transacción
                conn.commit()

                print("Pedido guardado correctamente y el número de pedidos del cliente ha sido incrementado.")
            else:
                print("Error: Usuario no encontrado.")
        except sqlite3.Error as e:
            print(f"Error al guardar el pedido: {e}")
        finally:
            conn.close()

    def guardar_credenciales(self, usuario, contraseña, nombre, apellido, pin):
        """Guarda las credenciales de un cliente en la base de datos."""
        conn = None  # Inicializamos conn para asegurarnos de que siempre exista
        try:
            # Validar que el nombre y apellido sean solo texto, sin espacios
            if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$", nombre):
                return {"status": "error", "message": "El nombre solo puede contener letras, sin espacios."}
            if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$", apellido):
                return {"status": "error", "message": "El apellido solo puede contener letras, sin espacios."}

            # Validar que el nombre de usuario no sea solo numérico y no contenga espacios
            if usuario.isnumeric():
                return {"status": "error", "message": "El nombre de usuario no puede ser solo numérico."}

            if " " in usuario:
                return {"status": "error", "message": "El nombre de usuario no puede contener espacios."}

            # Validar que la contraseña no tenga espacios
            if " " in contraseña:
                    return {"status": "error", "message": "La contraseña no puede contener espacios."}

            # Convertir la primera letra del nombre y apellido a mayúscula
            nombre = nombre.capitalize()
            apellido = apellido.capitalize()

            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Verificar si el usuario ya existe en la base de datos
            cursor.execute('''SELECT COUNT(*) FROM clientes WHERE user_cli = ?''', (usuario,))
            result = cursor.fetchone()

            if result[0] > 0:
                return {"status": "error", "message": "El nombre de usuario ya está en uso. Por favor, elija otro."}

            # Insertar los datos si el usuario no existe, incluyendo el valor de cantidadPedidos como 0
            cursor.execute(''' 
                   INSERT INTO clientes (user_cli, pass_cli, nombre, apellido, pin, cantidadPedidos) 
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''', (usuario, contraseña, nombre, apellido, pin, 0))  # Establecer cantidadPedidos a 0 por defecto

            # Confirmar la transacción
            conn.commit()

            print("Credenciales guardadas correctamente.")
            return {"status": "success", "message": "Credenciales guardadas correctamente."}

        except sqlite3.Error as e:
            # Manejo de errores de base de datos
            print(f"Error al guardar las credenciales: {e}")
            return {"status": "error", "message": f"Error al guardar las credenciales: {e}"}

        finally:
            # Asegurarse de cerrar la conexión solo si fue creada
            if conn:
                conn.close()



    # Metodos para manejar operaciones

    def cambiar_contrasena(self, pin, nueva_contrasena):
        """Actualiza la contraseña de un cliente dado su PIN."""
        cliente = self.obtener_cliente_por_pin(pin)

        if cliente:
            try:
                # Actualizar la contraseña del cliente en la base de datos
                with sqlite3.connect("pedidos.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                               UPDATE clientes
                               SET pass_cli = ?
                               WHERE pin = ?
                           """, (nueva_contrasena, pin))
                    conn.commit()

                    # Verificar si la actualización fue exitosa
                    if cursor.rowcount > 0:
                        return {"status": "success", "message": "Contraseña actualizada exitosamente."}
                    else:
                        return {"status": "error",
                                "message": "No se pudo actualizar la contraseña. Intente nuevamente."}
            except sqlite3.OperationalError as e:
                print(f"Error al actualizar la contraseña: {e}")
                return {"status": "error", "message": "Hubo un error al actualizar la contraseña."}
        else:
            return {"status": "error", "message": "No se encontró un cliente con ese PIN."}

    def incrementar_pedidos(self, usuario):
        conn = None  # Inicializamos conn para asegurarnos de que siempre exista
        """Incrementa el número de pedidos del cliente en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Incrementar el numeroPedidos para el usuario especificado
            cursor.execute('''
                UPDATE clientes SET numeroPedidos = numeroPedidos + 1 WHERE user_cli = ?
            ''', (usuario,))

            # Confirmar la transacción
            conn.commit()

            print(f"El número de pedidos del usuario {usuario} se ha incrementado.")
            return {"status": "success", "message": "Número de pedidos incrementado correctamente."}

        except sqlite3.Error as e:
            print(f"Error al incrementar el número de pedidos: {e}")
            return {"status": "error", "message": f"Error al incrementar el número de pedidos: {e}"}

        finally:
            if conn:
                conn.close()

    def manejar_click(self, usuario, contraseña, page):
        resultado = self.verificar_user(usuario, contraseña)
        return resultado

    def verificar_user(self, usuario, contraseña):
        """Verifica las credenciales de un usuario (cliente o artista)."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Verificar en 'artista'
            cursor.execute("SELECT * FROM artista WHERE user_artista = ? AND pass_artista = ?", (usuario, contraseña))
            if cursor.fetchone():
                return "ventana4"

            # Verificar en 'clientes'
            cursor.execute("SELECT * FROM clientes WHERE user_cli = ? AND pass_cli = ?", (usuario, contraseña))
            if cursor.fetchone():
                return "ventana5"

            return None
        except sqlite3.Error as e:
            print(f"Error al verificar usuario: {e}")
            return None
        finally:
            conn.close()

    def actualizar_precio_pedido(self, pedido_id, precio):
        """Actualiza el precio de un pedido y lo suma/resta al totalEnCuenta del artista asociado dependiendo de la diferencia."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Asumimos que el artista es único, por lo que podemos establecer el id_artista directamente
            # Si el id_artista depende del usuario logueado o algo similar, cámbialo aquí
            id_artista = 1  # Aquí se puede poner la lógica para obtener el id del artista

            # Obtener el precio actual del pedido (si existe)
            cursor.execute("SELECT precio FROM pedidos WHERE id = ?", (pedido_id,))
            precioV = cursor.fetchone()

            if precioV:
                # Si ya existe un precio para el pedido
                precioV = precioV[0]

                # Comparar el precio actual con el nuevo precio
                if precio > precioV:
                    ajuste = precio - precioV  # Si el nuevo precio es mayor
                    # Sumar el ajuste al totalEnCuenta del artista
                    cursor.execute("UPDATE artista SET totalEnCuenta = totalEnCuenta + ? WHERE id = ?",
                                   (ajuste, id_artista))
                elif precio < precioV:
                    ajuste = precioV - precio  # Si el nuevo precio es menor
                    # Restar el ajuste al totalEnCuenta del artista
                    cursor.execute("UPDATE artista SET totalEnCuenta = totalEnCuenta - ? WHERE id = ?",
                                   (ajuste, id_artista))
                # Si los precios son iguales, no hacemos nada
            else:
                # Si el pedido no tiene precio asignado (precioV es None)
                precioV = 0  # No hay precio previamente guardado

            # Actualizar el precio del pedido con el nuevo valor
            cursor.execute("UPDATE pedidos SET precio = ? WHERE id = ?", (precio, pedido_id))

            # Confirmar los cambios
            conn.commit()
            print("Precio actualizado y reflejado correctamente en la cuenta del artista.")

        except sqlite3.Error as e:
            print(f"Error al actualizar el precio: {e}")
        finally:
            if conn:
                conn.close()

    #Metodos para mostrar

    def mostrar_clientes_top_10(self, page, clientes):
        """Muestra los 10 clientes con más pedidos en un ListView."""
        if clientes["status"] == "success":
            # Crear el ListView con los clientes
            list_view = ft.ListView()

            # Agregar cada cliente al ListView
            for cliente in clientes["clientes"]:
                list_view.controls.append(ft.Text(cliente))

            # Añadir el ListView a la página
            page.add(list_view)
            page.update()
        else:
            page.add(ft.Text(clientes["message"]))
            page.update()


    # Metodos para obtener pedidos y datos de la BD

    def obtener_pedidos(self, usuario, tipo):
        """Obtiene los pedidos según el tipo (cliente o artista)."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                if tipo == 'cliente':
                    cursor.execute("SELECT id_cli FROM clientes WHERE user_cli=?", (usuario,))
                    resultado = cursor.fetchone()
                    if resultado:
                        cursor.execute('''
                            SELECT id, tamano, estilo, tonalidades, material, tipo, precio, nombreCliente, apellidoCliente, userCliente
                            FROM pedidos 
                            WHERE id_cli = ?
                        ''', (resultado[0],))
                        return cursor.fetchall()

                elif tipo == 'artista':
                    cursor.execute('''
                        SELECT id, tamano, estilo, tonalidades, material, tipo, precio, nombreCliente, apellidoCliente, userCliente
                        FROM pedidos
                    ''')
                    resultado = cursor.fetchall()
                    print(resultado)
                    return resultado

                return []

        except sqlite3.Error as e:
            print(f"Error al obtener pedidos: {e}")
            return []

    def obtener_datos_usuario(self, usuario, contraseña, page):
        """
        Método que obtiene el nombre y apellido del usuario, basado en sus credenciales,
        y los retorna si es válido. Si no es válido, retorna None.
        Primero verifica en la tabla de 'clientes', y luego en la tabla de 'artistas'.
        """
        if not self.verificar_user(usuario, contraseña):  # Si las credenciales no son correctas
            page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña incorrectos"))
            page.snack_bar.open = True
            page.update()
            return None

        try:
            # Conectar a la base de datos para obtener el nombre y apellido del usuario
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # Primero verificamos en la tabla 'clientes'
                cursor.execute("""
                    SELECT nombre, apellido
                    FROM clientes
                    WHERE user_cli = ? AND pass_cli = ?
                """, (usuario, contraseña))

                datos_usuario = cursor.fetchone()  # Recupera los datos (nombre y apellido)

                if datos_usuario:
                    nombre, apellido = datos_usuario
                    # Guardar el nombre y apellido en la sesión (si es necesario)
                    page.session.set("nombre", nombre)
                    page.session.set("apellido", apellido)

                    return {"nombre": nombre, "apellido": apellido}  # Retorna los datos del usuario
                else:
                    # Si no se encuentra en 'clientes', verificar en la tabla 'artistas'
                    cursor.execute("""
                        SELECT nombre, apellido
                        FROM artista
                        WHERE user_artista = ? AND pass_artista = ?
                    """, (usuario, contraseña))

                    datos_usuario = cursor.fetchone()  # Recupera los datos (nombre y apellido)

                    if datos_usuario:
                        nombre, apellido = datos_usuario
                        # Guardar el nombre y apellido en la sesión (si es necesario)
                        page.session.set("nombre", nombre)
                        page.session.set("apellido", apellido)

                        return {"nombre": nombre, "apellido": apellido}  # Retorna los datos del artista
                    else:
                        # Si no se encuentra el usuario ni en 'clientes' ni en 'artistas'
                        page.snack_bar = ft.SnackBar(ft.Text("Usuario no encontrado"))
                        page.snack_bar.open = True
                        page.update()
                        return None

        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            page.snack_bar = ft.SnackBar(ft.Text("Error al consultar la base de datos"))
            page.snack_bar.open = True
            page.update()
            return None

    def obtener_top_10_clientes(self):
        """Obtiene los 10 clientes que más pedidos han hecho (con al menos 1 pedido)."""
        conn = None
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Realizar la consulta para contar los pedidos de cada cliente y ordenarlos de mayor a menor
            cursor.execute('''
                SELECT c.nombre, c.apellido, COUNT(p.id) AS cantidad_pedidos
                FROM clientes c
                LEFT JOIN pedidos p ON c.id_cli = p.id_cli
                WHERE c.cantidadPedidos > 0  -- Filtrar solo clientes con más de 0 pedidos
                GROUP BY c.id_cli
                ORDER BY cantidad_pedidos DESC
                LIMIT 10
            ''')

            # Obtener los resultados
            resultados = cursor.fetchall()

            if not resultados:
                return {"status": "error", "message": "No se encontraron clientes con pedidos."}

            # Construir una lista con los clientes más activos
            clientes_top_10 = []
            for resultado in resultados:
                nombre_completo = f"{resultado[0]} {resultado[1]}"
                cantidad_pedidos = resultado[2]
                clientes_top_10.append(f"{nombre_completo}: {cantidad_pedidos} pedidos")

            return {"status": "success", "clientes": clientes_top_10}

        except sqlite3.Error as e:
            print(f"Error al obtener los clientes: {e}")
            return {"status": "error", "message": f"Error al obtener los clientes: {e}"}

        finally:
            if conn:
                conn.close()

    def obtener_resumen_datos(self):
        """Obtener el número total de clientes, pedidos y el total en cuenta de los artistas."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Obtener el total de clientes
            cursor.execute("SELECT COUNT(*) FROM clientes")
            cantidad_clientes = cursor.fetchone()[0]

            # Obtener el total de pedidos
            cursor.execute("SELECT COUNT(*) FROM pedidos")
            cantidad_pedidos = cursor.fetchone()[0]

            # Obtener el total acumulado en la cuenta de todos los artistas
            cursor.execute("SELECT SUM(totalEnCuenta) FROM artista")
            total_en_cuenta = cursor.fetchone()[0]

            # Manejar el caso en el que no haya artistas o total sea NULL
            if total_en_cuenta is None:
                total_en_cuenta = 0.0

            print(f"Clientes: {cantidad_clientes}, Pedidos: {cantidad_pedidos}, Total en cuenta: {total_en_cuenta}")
            return cantidad_clientes, cantidad_pedidos, total_en_cuenta

        except sqlite3.Error as e:
            print(f"Error al obtener los datos: {e}")
            return 0, 0, 0.0

        finally:
            conn.close()

    def obtener_cliente_por_pin(self, pin):
        """Obtiene los datos de un cliente dado su PIN."""
        try:
            with sqlite3.connect("pedidos.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                       SELECT id_cli, user_cli, pass_cli, nombre, apellido, pin
                       FROM clientes
                       WHERE pin = ?
                   """, (pin,))
                resultado = cursor.fetchone()
                if resultado:
                    return {
                        "id_cli": resultado[0],
                        "user_cli": resultado[1],
                        "pass_cli": resultado[2],
                        "nombre": resultado[3],
                        "apellido": resultado[4],
                        "pin": resultado[5],
                    }
                else:
                    return None  # Si no se encuentra un cliente con el PIN dado
        except sqlite3.OperationalError as e:
            print(f"Error al consultar la base de datos: {e}")
            return None

    def obtener_pedidos_db(self, usuario, tipo):
        if tipo == 'cliente':
            try:
                with sqlite3.connect("pedidos.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_cli FROM clientes WHERE user_cli=?", (usuario,))
                    resultado = cursor.fetchone()
                    usuario_id = resultado[0]
                    cursor.execute("""
                        SELECT id, tamano, estilo, tonalidades, material, tipo, precio, nombreCliente, apellidoCliente, userCliente 
                        FROM pedidos 
                        WHERE id_cli = ?
                    """, (usuario_id,))
                    return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f"Error al consultar la base de datos: {e}")
                return []
        elif tipo == 'artista':
            try:
                with sqlite3.connect("pedidos.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, tamano, estilo, tonalidades, material, tipo, precio, nombreCliente, apellidoCliente, userCliente 
                        FROM pedidos
                    """)
                    return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f"Error al consultar la base de datos: {e}")
                return []

    def obtener_pedidos_con_precio_0(self, usuario, tipo):
        if tipo == 'cliente':
            try:
                with sqlite3.connect("pedidos.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_cli FROM clientes WHERE user_cli=?", (usuario,))
                    resultado = cursor.fetchone()
                    if resultado:
                        usuario_id = resultado[0]
                        cursor.execute("""
                            SELECT id, tamano, estilo, tonalidades, material, tipo, precio, nombreCliente, apellidoCliente, userCliente 
                            FROM pedidos 
                            WHERE id_cli = ? AND precio = 0.00
                        """, (usuario_id,))
                        return cursor.fetchall()
                    else:
                        return []
            except sqlite3.OperationalError as e:
                print(f"Error al consultar la base de datos: {e}")
                return []
        elif tipo == 'artista':
            try:
                with sqlite3.connect("pedidos.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, tamano, estilo, tonalidades, material, tipo, precio, nombreCliente, apellidoCliente, userCliente 
                        FROM pedidos
                        WHERE precio = 0.00
                    """)
                    return cursor.fetchall()
            except sqlite3.OperationalError as e:
                print(f"Error al consultar la base de datos: {e}")
                return []