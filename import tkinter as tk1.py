import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QAction, QMessageBox, QTabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Simulador de Combustible")
        self.setGeometry(100, 100, 800, 600)

        # Configuración de las pestañas
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.individual_tab = QWidget()
        self.resistencia_tab = QWidget()
        
        self.tab_widget.addTab(self.individual_tab, "Individual")
        self.tab_widget.addTab(self.resistencia_tab, "Resistencia")

        # Configuración de la pestaña "Individual"
        self.setup_individual_tab()

        # Configuración de la pestaña "Resistencia"
        self.setup_resistencia_tab()

        # Menú para mostrar la versión
        self.menu_bar = self.menuBar()
        self.version_menu = self.menu_bar.addMenu("Ayuda")

        self.version_action = QAction("Mostrar Versión", self)
        self.version_action.triggered.connect(self.mostrar_version)
        self.version_menu.addAction(self.version_action)

    def mostrar_version(self):
        QMessageBox.information(self, "Versión", "Versión 1.0 de la aplicación.")

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












