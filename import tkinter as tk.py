import os
from smbprotocol.connection import Connection
from smbprotocol.open import Open
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from pathlib import Path
import shutil

def autenticar_usuario(servidor, usuario, contraseña):
    try:
        connection = Connection(uuid=os.urandom(16), server=servidor, port=445)
        connection.connect()
        session = Session(connection, username=1234, password=1111)
        session.connect()
        return connection, session
    except Exception as e:
        print(f"Error de autenticación: {e}")
        return None, None

def verificar_actualizacion(connection, session, ruta_servidor, version_actual):
    try:
        tree = TreeConnect(session, f"\\\\{connection.server}\\{ruta_servidor}")
        tree.connect()
        
        with Open(tree, "version.txt", "rb") as archivo_version:
            version_servidor = archivo_version.read().decode("utf-8").strip()
        
        if version_servidor > version_actual:
            print(f"Actualización disponible: {version_servidor}")
            return True
        return False
    except Exception as e:
        print(f"Error al verificar la actualización: {e}")
        return False

def actualizar_aplicacion(connection, session, ruta_servidor, ruta_app):
    try:
        tree = TreeConnect(session, f"\\\\{connection.server}\\{ruta_servidor}")
        tree.connect()
        
        with Open(tree, "app.exe", "rb") as nueva_app:
            with open(ruta_app, "wb") as archivo_local:
                shutil.copyfileobj(nueva_app, archivo_local)
        
        print("Aplicación actualizada con éxito")
    except Exception as e:
        print(f"Error al actualizar la aplicación: {e}")

if __name__ == "__main__":
    # Datos del servidor y aplicación
    SERVIDOR = "NOMBRE_SERVIDOR"
    RUTA_SERVIDOR = "CarpetaCompartida"
    VERSION_ACTUAL = "1.0.0"
    RUTA_APP = r"C:\Ruta\A\Tu\app.exe"

    # Credenciales de usuario
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    # Autenticación y actualización
    connection, session = autenticar_usuario(SERVIDOR, usuario, contraseña)
    if connection and session:
        print("Autenticación exitosa")
        if verificar_actualizacion(connection, session, RUTA_SERVIDOR, VERSION_ACTUAL):
            actualizar_aplicacion(connection, session, RUTA_SERVIDOR, RUTA_APP)
        else:
            print("No se requiere actualización")
        
        # Desconexión del servidor
        connection.disconnect()
    else:
        print("Error de autenticación. No se puede acceder al servidor de actualizaciones.")


    def setup_individual_tab(self):
        layout = QGridLayout()

        # Campos para la pestaña Individual
        layout.addWidget(QLabel("Consumo (L/vuelta):"), 0, 0)
        self.consumo_individual = QLineEdit()
        layout.addWidget(self.consumo_individual, 0, 1)

        layout.addWidget(QLabel("Capacidad del tanque (L):"), 1, 0)
        self.capacidad_individual = QLineEdit()
        layout.addWidget(self.capacidad_individual, 1, 1)

        layout.addWidget(QLabel("Duración de la carrera (min):"), 2, 0)
        self.duracion_individual = QLineEdit()
        layout.addWidget(self.duracion_individual, 2, 1)

        layout.addWidget(QLabel("Tiempo promedio por vuelta (s):"), 3, 0)
        self.tiempo_vuelta_individual = QLineEdit()
        layout.addWidget(self.tiempo_vuelta_individual, 3, 1)

        # Campo para mostrar el resultado del cálculo
        layout.addWidget(QLabel("Combustible necesario (L):"), 4, 0)
        self.resultado_individual = QLabel("0")
        layout.addWidget(self.resultado_individual, 4, 1)

        # Botón para calcular
        self.btn_calcular_individual = QPushButton("Calcular Individual")
        self.btn_calcular_individual.clicked.connect(self.calcular_combustible_individual)
        layout.addWidget(self.btn_calcular_individual, 5, 0, 1, 2)

        self.individual_tab.setLayout(layout)

    def setup_resistencia_tab(self):
        layout = QGridLayout()

        # Campos para la pestaña Resistencia
        layout.addWidget(QLabel("Consumo (L/vuelta):"), 0, 0)
        self.consumo_resistencia = QLineEdit()
        layout.addWidget(self.consumo_resistencia, 0, 1)

        layout.addWidget(QLabel("Capacidad del tanque (L):"), 1, 0)
        self.capacidad_resistencia = QLineEdit()
        layout.addWidget(self.capacidad_resistencia, 1, 1)

        layout.addWidget(QLabel("Duración de la carrera (min):"), 2, 0)
        self.duracion_resistencia = QLineEdit()
        layout.addWidget(self.duracion_resistencia, 2, 1)

        layout.addWidget(QLabel("Tiempo promedio por vuelta (s):"), 3, 0)
        self.tiempo_vuelta_resistencia = QLineEdit()
        layout.addWidget(self.tiempo_vuelta_resistencia, 3, 1)

        # Campo para mostrar el resultado del cálculo
        layout.addWidget(QLabel("Combustible necesario (L):"), 4, 0)
        self.resultado_resistencia = QLabel("0")
        layout.addWidget(self.resultado_resistencia, 4, 1)

        # Botón para calcular
        self.btn_calcular_resistencia = QPushButton("Calcular Resistencia")
        self.btn_calcular_resistencia.clicked.connect(self.calcular_combustible_resistencia)
        layout.addWidget(self.btn_calcular_resistencia, 5, 0, 1, 2)

        self.resistencia_tab.setLayout(layout)

    def autenticar_usuario(self, servidor, usuario, contraseña):
        try:
            win32net.NetUseAdd(None, 2, {
                "remote": f"\\\\{servidor}",
                "username": usuario,
                "password": contraseña
            })
            return True
        except:
            return False

    def verificar_actualizacion(self, ruta_servidor, version_actual):
        archivo_version = Path(ruta_servidor) / "version.txt"
        if archivo_version.exists():
            with open(archivo_version, "r") as f:
                version_servidor = f.read().strip()
            
            if version_servidor > version_actual:
                return True
        return False

    def actualizar_aplicacion(self, ruta_servidor, ruta_app):
        nueva_app = Path(ruta_servidor) / "app.exe"
        if nueva_app.exists():
            shutil.copy(nueva_app, ruta_app)
            QMessageBox.information(self, "Actualización", "Aplicación actualizada con éxito.")
        else:
            QMessageBox.warning(self, "Error", "Archivo de actualización no encontrado en el servidor.")

    def verificar_actualizacion_app(self):
        servidor = "NOMBRE_SERVIDOR"
        ruta_servidor = f"\\\\{servidor}\\CarpetaCompartida"
        version_actual = "1.0.0"
        ruta_app = r"C:\Ruta\A\Tu\app.exe"

        usuario, ok = QInputDialog.getText(self, "Autenticación", "Ingrese su nombre de usuario:")
        if not ok:
            return
        contraseña, ok = QInputDialog.getText(self, "Autenticación", "Ingrese su contraseña:", QLineEdit.Password)
        if not ok:
            return

        if self.autenticar_usuario(servidor, usuario, contraseña):
            if self.verificar_actualizacion(ruta_servidor, version_actual):
                self.actualizar_aplicacion(ruta_servidor, ruta_app)
            else:
                QMessageBox.information(self, "Actualización", "No hay actualizaciones disponibles.")
            win32net.NetUseDel(None, ruta_servidor, 0)
        else:
            QMessageBox.warning(self, "Error de Autenticación", "No se pudo autenticar el usuario.")

    def calcular_combustible_individual(self):
        try:
            consumo = float(self.consumo_individual.text())
            duracion = float(self.duracion_individual.text())
            tiempo_vuelta = float(self.tiempo_vuelta_individual.text())

            vueltas_totales = (duracion * 60) / tiempo_vuelta
            combustible_necesario = consumo * vueltas_totales

            self.resultado_individual.setText(f"{combustible_necesario:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingresa valores numéricos válidos.")

    def calcular_combustible_resistencia(self):
        try:
            consumo = float(self.consumo_resistencia.text())
            duracion = float(self.duracion_resistencia.text())
            tiempo_vuelta = float(self.tiempo_vuelta_resistencia.text())

            vueltas_totales = (duracion * 60) / tiempo_vuelta
            combustible_necesario = consumo * vueltas_totales

            self.resultado_resistencia.setText(f"{combustible_necesario:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingresa valores numéricos válidos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())












