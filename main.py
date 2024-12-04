import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Administración interna de MiGas"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Contenedor donde se mostrará el contenido de las pestañas
    tab_contenido = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.START,
    )

    # Crear widget de la imagen
    imagen = ft.Image(
        src="https://images.pexels.com/photos/12203738/pexels-photo-12203738.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",  # Assuming image is in an 'images' subdirectory
        width=650,
        height=400,
        fit=ft.ImageFit.CONTAIN
    )

    # Función para manejar el cambio de pestañas
    def cambiar_pagina(e):
        tab_contenido.controls.clear()

        # Pestaña de Inicio
        if tabs.tabs[tabs.selected_index].text == "Inicio":
            tab_contenido.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("¡Bienvenido a tu centro de operaciones!", size=24, weight="bold"),
                        ft.Text("Desde aquí podrás controlar y optimizar todos los procesos de tu estación de servicio."),
                        imagen,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar verticalmente
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
                )
            )
        tab_contenido.update()
### 
### Pestaña de Administración de Usuarios ### 
### 

        if tabs.tabs[tabs.selected_index].text == "Administración de Usuarios":
            
            ### Función para añadir un usuario
            
            def añadir_usuario(e):
                nombre = ft.TextField(label="Nombre")
                email = ft.TextField(label="E-mail")
                password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)


                # Guardar usuario
                def guardar_proyecto(ev):
                    try:
                        data = {
                        "nombre": nombre.value,
                        "email": email.value,
                        "password": password.value,
                    }
                        response = requests.post("https://projectfbd-production.up.railway.app/usuarios/", json=data)
                        response.raise_for_status()
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text("Usuario añadido exitosamente.", color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREEN,
                        )
                        page.snack_bar.open = True
                        cambiar_pagina(None)
                    except requests.RequestException as error:
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(f"Error al añadir usuario: {error}", color=ft.colors.WHITE),
                            bgcolor=ft.colors.RED,
                        )
                        page.snack_bar.open = True
                    page.update()

                # Diálogo para añadir usuario
                page.dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Añadir nuevo usuario"),
                    content=ft.Column([nombre, email, password]),
                    actions=[
                        ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=guardar_proyecto),
                        ft.ElevatedButton("Cancelar", icon=ft.icons.CANCEL, on_click=lambda ev: cerrar_dialogo()),
                 ],
                 actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog.open = True
                page.update()
            
            def cerrar_dialogo():
                page.dialog.open = False
                page.update()
                
            
            ### Función para modificar un usuario
            
            def modificar_usuario(e, usuario):
                nombre = ft.TextField(label="Nombre", value=usuario["nombre"])
                email = ft.TextField(label="Email", value=usuario["email"])
                password = ft.TextField(label="Password", value="")

                # Guardar cambios
                def guardar_cambios(ev):
                    try:
                        data = {"nombre": nombre.value, "email": email.value, "password": password.value}
                        response = requests.put(
                            f"https://projectfbd-production.up.railway.app/usuarios/{usuario['id']}/", json=data
                        )
                        response.raise_for_status()
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text("Usuario modificado exitosamente.", color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREEN,
                        )
                        page.snack_bar.open = True
                        cambiar_pagina(None)
                    except requests.RequestException as error:
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(f"Error al modificar usuario: {error}", color=ft.colors.WHITE),
                            bgcolor=ft.colors.RED,
                        )
                        page.snack_bar.open = True
                    page.update()

                # Diálogo para modificar usuario
                page.dialog = ft.AlertDialog(
                   modal=True,
                   title=ft.Text(f"Modificar usuario ID: {usuario['id']}"),
                  content=ft.Column([nombre, email, password]),
                   actions=[
                       ft.ElevatedButton("Guardar cambios", icon=ft.icons.SAVE, on_click=guardar_cambios),
                       ft.ElevatedButton("Cancelar", icon=ft.icons.CANCEL, on_click=lambda ev: cerrar_dialogo()),
                   ],
                   actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog.open = True
                page.update()
            
            def cerrar_dialogo():
                page.dialog.open = False
                page.update()

            
            ### Función para eliminar un usuario
            
            def eliminar_usuario(e, id):
                try:
                    response = requests.delete(f"https://projectfbd-production.up.railway.app/usuarios/{id}/")
                    response.raise_for_status()
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Usuario eliminado exitosamente.", color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREEN,
                    )
                    page.snack_bar.open = True
                    cambiar_pagina(None)
                except requests.RequestException as error:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Error al eliminar usuario: {error}", color=ft.colors.WHITE),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
                page.update()


            # Mostrar un spinner antes de cargar
            spinner = ft.ProgressRing()
            tab_contenido.controls.append(spinner)
            tab_contenido.update()

            ### Función para cargar usuarios
            
            try:
                response = requests.get("https://projectfbd-production.up.railway.app/usuarios/")
                spinner.visible = False
                response.raise_for_status()
                usuarios = response.json()

                filas = [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(usuario["id"]))),
                            ft.DataCell(ft.Text(usuario["nombre"])),
                            ft.DataCell(ft.Text(usuario["email"])),
                            ft.DataCell(
                                ft.ElevatedButton(
                                    text="Modificar",
                                    icon=ft.icons.EDIT,
                                    on_click=lambda e, u=usuario: modificar_usuario(e, u),
                                )
                            ),
                            ft.DataCell(
                                ft.ElevatedButton(
                                    text="Eliminar",
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, id=usuario["id"]: eliminar_usuario(e, id),
                                )
                            ),
                        ]
                    )
                    for usuario in usuarios
                ]

                tab_contenido.controls.append(
                    ft.Column(
                        controls=[
                            ft.Text("Gestión de usuarios", size=20, weight="bold"),
                            ft.TextField(label="Buscar usuario"),
                            ft.ElevatedButton("Añadir usuario", icon=ft.icons.ADD, on_click=lambda e: añadir_usuario(e)),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("ID")),
                                    ft.DataColumn(ft.Text("Nombre")),
                                    ft.DataColumn(ft.Text("Email")),
                                    ft.DataColumn(ft.Text("Modificar")),
                                    ft.DataColumn(ft.Text("Eliminar")),
                                ],
                                rows=filas,
                            ),
                        ]
                    )
                )
            except requests.RequestException as error:
                tab_contenido.controls.append(
                    ft.Text(f"Error al cargar usuarios: {error}", color=ft.colors.RED)
                )

### 
### Pestaña de Administración de Proyectos ### 
### 

        elif tabs.tabs[tabs.selected_index].text == "Administración de Proyectos":

            ### Función para añadir un proyecto
            
            def añadir_proyecto(e):
                nombre = ft.TextField(label="Nombre")
                descripcion = ft.TextField(label="Descripción")

                # Guardar proyecto
                def guardar_proyecto(ev):
                    try:
                        data = {"nombre": nombre.value, "descripcion": descripcion.value}
                        response = requests.post("https://projectfbd-production.up.railway.app/proyectos/", json=data)
                        response.raise_for_status()
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text("Proyecto añadido exitosamente.", color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREEN,
                        )
                        page.snack_bar.open = True
                        cambiar_pagina(None)
                    except requests.RequestException as error:
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(f"Error al añadir proyecto: {error}", color=ft.colors.WHITE),
                            bgcolor=ft.colors.RED,
                        )
                        page.snack_bar.open = True
                    page.update()

                # Diálogo para añadir proyecto
                page.dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Añadir nuevo proyecto"),
                    content=ft.Column([nombre, descripcion]),
                    actions=[
                        ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=guardar_proyecto),
                        ft.ElevatedButton("Cancelar", icon=ft.icons.CANCEL, on_click=lambda ev: cerrar_dialogo()),
                 ],
                 actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog.open = True
                page.update()
            
            def cerrar_dialogo():
                page.dialog.open = False
                page.update()
            
            ### Función para modificar un proyecto
            
            def editar_proyecto(e, proyecto):
                 # Campos editables
                 nombre = ft.TextField(label="Nombre", value=proyecto["nombre"])
                 descripcion = ft.TextField(label="Descripción", value=proyecto["descripcion"])

                 # Guardar cambios en la API
                 def guardar_cambios(ev):
                     try:
                         data = {
                             "nombre": nombre.value,
                             "descripcion": descripcion.value,
                         }
                         response = requests.put(
                             f"https://projectfbd-production.up.railway.app/proyectos/{proyecto['id']}/",
                             json=data,
                         )
                         response.raise_for_status()
                         page.dialog.open = False
                         page.snack_bar = ft.SnackBar(
                             content=ft.Text("Proyecto modificado exitosamente.", color=ft.colors.WHITE),
                             bgcolor=ft.colors.GREEN,
                         )
                         page.snack_bar.open = True
                         cambiar_pagina(None)  # Refrescar la tabla de proyectos
                     except requests.RequestException as error:
                         page.dialog.open = False
                         page.snack_bar = ft.SnackBar(
                             content=ft.Text(f"Error al modificar proyecto: {error}", color=ft.colors.WHITE),
                             bgcolor=ft.colors.RED,
                         )
                         page.snack_bar.open = True
                     page.update()

                 # Diálogo para modificar proyecto
                 page.dialog = ft.AlertDialog(
                     modal=True,
                     title=ft.Text(f"Modificar proyecto ID: {proyecto['id']}"),
                     content=ft.Column([nombre, descripcion]),
                     actions=[
                         ft.ElevatedButton("Guardar cambios", icon=ft.icons.SAVE, on_click=guardar_cambios),
                         ft.ElevatedButton("Cancelar", icon=ft.icons.CANCEL, on_click=lambda ev: cerrar_dialogo()),
                     ],
                     actions_alignment=ft.MainAxisAlignment.END,
                 )
                 page.dialog.open = True
                 page.update()

            ### Función para eliminar un proyecto
            
            def eliminar_proyecto(e, id):
                try:
                    response = requests.delete(f"https://projectfbd-production.up.railway.app/proyectos/{id}/")
                    response.raise_for_status()
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Proyecto eliminado exitosamente.", color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREEN,
                    )
                    page.snack_bar.open = True
                    cambiar_pagina(None)
                except requests.RequestException as error:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Error al eliminar proyecto: {error}", color=ft.colors.WHITE),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
                page.update()

            # Mostrar un spinner antes de cargar
            spinner = ft.ProgressRing()
            tab_contenido.controls.append(spinner)
            tab_contenido.update()
            
            ### Función para cargar proyectos
            
            def cargar_proyectos():
                try:
                    response = requests.get("https://projectfbd-production.up.railway.app/proyectos/")
                    spinner.visible = False
                    response.raise_for_status()
                    proyectos = response.json()

                    filas = [
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(proyecto["id"]))),
                                ft.DataCell(ft.Text(proyecto["nombre"])),
                                ft.DataCell(ft.Text(proyecto["descripcion"])),
                                ft.DataCell(
                                    ft.ElevatedButton(
                                        text="Modificar",
                                        icon=ft.icons.EDIT,
                                        on_click=lambda e, p=proyecto: editar_proyecto(e, p),
                                    )
                                ),
                                ft.DataCell(
                                    ft.ElevatedButton(
                                        text="Eliminar",
                                        icon=ft.icons.DELETE,
                                        on_click=lambda e, id=proyecto["id"]: eliminar_proyecto(e, id),
                                    )
                                ),
                            ]
                        )
                        for proyecto in proyectos
                    ]

                    tab_contenido.controls.append(
                        ft.Column(
                            controls=[
                                ft.Text("Gestión de proyectos", size=20, weight="bold"),
                                ft.TextField(label="Buscar proyecto"),
                                ft.ElevatedButton("Añadir proyecto", icon=ft.icons.ADD, on_click=añadir_proyecto),
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("ID")),
                                        ft.DataColumn(ft.Text("Nombre")),
                                        ft.DataColumn(ft.Text("Descripción")),
                                        ft.DataColumn(ft.Text("Modificar")),
                                        ft.DataColumn(ft.Text("Eliminar")),
                                    ],
                                    rows=filas,
                                ),
                            ]
                        )
                    )
                except requests.RequestException as error:
                    tab_contenido.controls.append(
                        ft.Text(f"Error al cargar proyectos: {error}", color=ft.colors.RED)
                    )

            cargar_proyectos()
### 
### Pestaña de Administración de Gasolineras ### 
### 

        elif tabs.tabs[tabs.selected_index].text == "Administración de Gasolineras":

            ### Función para añadir una gasolinera
            
            def añadir_gasolinera(e):
                nombre = ft.TextField(label="Nombre")
                direccion = ft.TextField(label="Dirección")

                # Guardar proyecto
                def guardar_gasolinera(ev):
                    try:
                        data = {"nombre": nombre.value, "direccion": direccion.value}
                        response = requests.post("https://projectfbd-production.up.railway.app/gasolineras/", json=data)
                        response.raise_for_status()
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text("Gasolineras añadida exitosamente.", color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREEN,
                        )
                        page.snack_bar.open = True
                        cambiar_pagina(None)
                    except requests.RequestException as error:
                        page.dialog.open = False
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(f"Error al añadir la gasolinera: {error}", color=ft.colors.WHITE),
                            bgcolor=ft.colors.RED,
                        )
                        page.snack_bar.open = True
                    page.update()

                # Diálogo para añadir gasolinera
                page.dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Añadir nueva Gasolinera"),
                    content=ft.Column([nombre, direccion]),
                    actions=[
                        ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=guardar_gasolinera),
                        ft.ElevatedButton("Cancelar", icon=ft.icons.CANCEL, on_click=lambda ev: cerrar_dialogo()),
                 ],
                 actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog.open = True
                page.update()
            
            def cerrar_dialogo():
                page.dialog.open = False
                page.update()
            
            ### Función para modificar una gasolinera
            
            def editar_gasolinera(e, gasolinera):
                 # Campos editables
                 nombre = ft.TextField(label="Nombre", value=gasolinera["nombre"])
                 direccion = ft.TextField(label="Dirección", value=gasolinera["direccion"])

                 # Guardar cambios en la API
                 def guardar_cambios(ev):
                     try:
                         data = {
                             "nombre": nombre.value,
                             "direccion": direccion.value,
                         }
                         response = requests.put(
                             f"https://projectfbd-production.up.railway.app/gasolineras/{gasolinera['id']}/",
                             json=data,
                         )
                         response.raise_for_status()
                         page.dialog.open = False
                         page.snack_bar = ft.SnackBar(
                             content=ft.Text("Gasolinera modificada exitosamente.", color=ft.colors.WHITE),
                             bgcolor=ft.colors.GREEN,
                         )
                         page.snack_bar.open = True
                         cambiar_pagina(None)  # Refrescar la tabla de gasolineras
                     except requests.RequestException as error:
                         page.dialog.open = False
                         page.snack_bar = ft.SnackBar(
                             content=ft.Text(f"Error al modificar la gasolinera: {error}", color=ft.colors.WHITE),
                             bgcolor=ft.colors.RED,
                         )
                         page.snack_bar.open = True
                     page.update()

                 # Diálogo para modificar gasolinera
                 page.dialog = ft.AlertDialog(
                     modal=True,
                     title=ft.Text(f"Modificar gasolinera ID: {gasolinera['id']}"),
                     content=ft.Column([nombre, direccion]),
                     actions=[
                         ft.ElevatedButton("Guardar cambios", icon=ft.icons.SAVE, on_click=guardar_cambios),
                         ft.ElevatedButton("Cancelar", icon=ft.icons.CANCEL, on_click=lambda ev: cerrar_dialogo()),
                     ],
                     actions_alignment=ft.MainAxisAlignment.END,
                 )
                 page.dialog.open = True
                 page.update()

            ### Función para eliminar una gasolinera
            
            def eliminar_gasolinera(e, id):
                try:
                    response = requests.delete(f"https://projectfbd-production.up.railway.app/gasolineras/{id}/")
                    response.raise_for_status()
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Gasolinera eliminado exitosamente.", color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREEN,
                    )
                    page.snack_bar.open = True
                    cambiar_pagina(None)
                except requests.RequestException as error:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Error al eliminar la gasolinera: {error}", color=ft.colors.WHITE),
                        bgcolor=ft.colors.RED,
                    )
                    page.snack_bar.open = True
                page.update()

            # Mostrar un spinner antes de cargar
            spinner = ft.ProgressRing()
            tab_contenido.controls.append(spinner)
            tab_contenido.update()
            
            ### Función para cargar gasolineras
            
            def cargar_gasolineras():
                try:
                    response = requests.get("https://projectfbd-production.up.railway.app/gasolineras/")
                    spinner.visible = False
                    response.raise_for_status()
                    gasolineras = response.json()

                    filas = [
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(gasolinera["id"]))),
                                ft.DataCell(ft.Text(gasolinera["nombre"])),
                                ft.DataCell(ft.Text(gasolinera["direccion"])),
                                ft.DataCell(
                                    ft.ElevatedButton(
                                        text="Modificar",
                                        icon=ft.icons.EDIT,
                                        on_click=lambda e, p=gasolinera: editar_gasolinera(e, p),
                                    )
                                ),
                                ft.DataCell(
                                    ft.ElevatedButton(
                                        text="Eliminar",
                                        icon=ft.icons.DELETE,
                                        on_click=lambda e, id=gasolinera["id"]: eliminar_gasolinera(e, id),
                                    )
                                ),
                            ]
                        )
                        for gasolinera in gasolineras
                    ]

                    tab_contenido.controls.append(
                        ft.Column(
                            controls=[
                                ft.Text("Gestión de gasolineras", size=20, weight="bold"),
                                ft.TextField(label="Buscar gasolineras"),
                                ft.ElevatedButton("Añadir gasolinera", icon=ft.icons.ADD, on_click=añadir_gasolinera),
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("ID")),
                                        ft.DataColumn(ft.Text("Nombre")),
                                        ft.DataColumn(ft.Text("Dirección")),
                                        ft.DataColumn(ft.Text("Modificar")),
                                        ft.DataColumn(ft.Text("Eliminar")),
                                    ],
                                    rows=filas,
                                ),
                            ]
                        )
                    )
                except requests.RequestException as error:
                    spinner.visible = False
                    tab_contenido.controls.append(
                        ft.Text(f"Error al cargar gasolineras: {error}", color=ft.colors.RED)
                    )

            cargar_gasolineras()
            
        tab_contenido.update()


    # Crear pestañas
    tabs = ft.Tabs(
        selected_index=0,
        on_change=cambiar_pagina,
        tabs=[
            ft.Tab(text="Inicio"),
            ft.Tab(text="Administración de Usuarios"),
            ft.Tab(text="Administración de Proyectos"),
            ft.Tab(text="Administración de Gasolineras"),
            ft.Tab(text="Administración de Vehiculos"),
        ],
    )

    # Agregar pestañas y contenido inicial
    page.add(tabs, tab_contenido)
    cambiar_pagina(None)

# Iniciar la aplicación en modo web
ft.app(target=main, view=ft.WEB_BROWSER)

# Punto de entrada para Vercel
def handler(event, context):
    return ft.app(target=main)