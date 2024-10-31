import sys
import json
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QRadioButton, QGroupBox, QComboBox,
    QSpinBox, QTableWidget, QTableWidgetItem, QMessageBox,
    QButtonGroup, QStatusBar, QDoubleSpinBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

class SingleRaceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.compounds = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Grupo de datos bÃ¡sicos
        basic_group = QGroupBox("Datos BÃ¡sicos")
        basic_layout = QVBoxLayout()

        # Capacidad de depÃ³sito
        tank_layout = QHBoxLayout()
        tank_label = QLabel("Capacidad del depÃ³sito (L):")
        self.tank_input = QDoubleSpinBox()
        self.tank_input.setRange(0, 999)
        self.tank_input.setDecimals(1)
        tank_layout.addWidget(tank_label)
        tank_layout.addWidget(self.tank_input)
        basic_layout.addLayout(tank_layout)

        # Consumo por vuelta
        consumption_layout = QHBoxLayout()
        consumption_label = QLabel("Consumo por vuelta (L):")
        self.consumption_input = QDoubleSpinBox()
        self.consumption_input.setRange(0, 100)
        self.consumption_input.setDecimals(2)
        consumption_layout.addWidget(consumption_label)
        consumption_layout.addWidget(self.consumption_input)
        basic_layout.addLayout(consumption_layout)

        # Tiempo por vuelta
        laptime_layout = QHBoxLayout()
        laptime_label = QLabel("Tiempo por vuelta (mm:ss.ms):")
        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 59)
        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(0, 59)
        self.milliseconds_input = QSpinBox()
        self.milliseconds_input.setRange(0, 999)
        laptime_layout.addWidget(laptime_label)
        laptime_layout.addWidget(self.minutes_input)
        laptime_layout.addWidget(QLabel(":"))
        laptime_layout.addWidget(self.seconds_input)
        laptime_layout.addWidget(QLabel("."))
        laptime_layout.addWidget(self.milliseconds_input)
        basic_layout.addLayout(laptime_layout)

        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)

        # Grupo de tipo de carrera
        race_type_group = QGroupBox("Tipo de Carrera")
        race_type_layout = QVBoxLayout()
        
        self.race_type_buttons = QButtonGroup()
        self.laps_radio = QRadioButton("Por Vueltas")
        self.time_radio = QRadioButton("Por Tiempo")
        self.race_type_buttons.addButton(self.laps_radio)
        self.race_type_buttons.addButton(self.time_radio)
        
        # Contenedor para datos de vueltas
        self.laps_container = QWidget()
        laps_layout = QHBoxLayout(self.laps_container)
        laps_layout.addWidget(QLabel("NÃºmero de vueltas:"))
        self.laps_input = QSpinBox()
        self.laps_input.setRange(1, 999)
        laps_layout.addWidget(self.laps_input)
        
        # Contenedor para datos de tiempo
        self.time_container = QWidget()
        time_layout = QHBoxLayout(self.time_container)
        time_layout.addWidget(QLabel("DuraciÃ³n (minutos):"))
        self.race_time_input = QSpinBox()
        self.race_time_input.setRange(1, 1440)  # MÃ¡ximo 24 horas
        time_layout.addWidget(self.race_time_input)
        
        race_type_layout.addWidget(self.laps_radio)
        race_type_layout.addWidget(self.laps_container)
        race_type_layout.addWidget(self.time_radio)
        race_type_layout.addWidget(self.time_container)
        
        self.laps_radio.toggled.connect(self.toggle_race_type)
        self.time_radio.toggled.connect(self.toggle_race_type)
        
        race_type_group.setLayout(race_type_layout)
        layout.addWidget(race_type_group)

        # Grupo de neumÃ¡ticos
        tyre_group = QGroupBox("GestiÃ³n de NeumÃ¡ticos")
        tyre_layout = QVBoxLayout()

        # Etiqueta de ayuda
        help_label = QLabel("Ayuda GestiÃ³n de neumÃ¡ticos")
        help_label.setStyleSheet("color: blue; text-decoration: underline; cursor: pointer;")
        help_label.mousePressEvent = self.show_help
        tyre_layout.addWidget(help_label)

        # Agregar nuevo compuesto
        add_tyre_layout = QHBoxLayout()
        self.compound_input = QComboBox()
        self.compound_input.addItems(["Blando", "Medio", "Duro", "Lluvia"])
        self.tyre_life_input = QSpinBox()
        self.tyre_life_input.setRange(1, 100)
        add_tyre_button = QPushButton("Agregar Compuesto")
        add_tyre_button.clicked.connect(self.add_tyre_compound)
        
        add_tyre_layout.addWidget(self.compound_input)
        add_tyre_layout.addWidget(QLabel("Vueltas efectivas:"))
        add_tyre_layout.addWidget(self.tyre_life_input)
        add_tyre_layout.addWidget(add_tyre_button)
        tyre_layout.addLayout(add_tyre_layout)

        # Lista de compuestos
        self.compound_list = QListWidget()
        self.compound_list.setDragDropMode(QListWidget.InternalMove)
        self.compound_list.model().rowsMoved.connect(self.update_compound_order)
        tyre_layout.addWidget(self.compound_list)

        # Botones para mover y eliminar compuestos
        button_layout = QHBoxLayout()
        self.move_up_button = QPushButton("Mover Arriba")
        self.move_up_button.clicked.connect(self.move_compound_up)
        self.move_down_button = QPushButton("Mover Abajo")
        self.move_down_button.clicked.connect(self.move_compound_down)
        self.delete_button = QPushButton("Eliminar Compuesto")
        self.delete_button.clicked.connect(self.delete_compound)
        
        button_layout.addWidget(self.move_up_button)
        button_layout.addWidget(self.move_down_button)
        button_layout.addWidget(self.delete_button)
        tyre_layout.addLayout(button_layout)

        tyre_group.setLayout(tyre_layout)
        layout.addWidget(tyre_group)

        # BotÃ³n de cÃ¡lculo
        calculate_button = QPushButton("Calcular Estrategia")
        calculate_button.clicked.connect(self.calculate_strategy)
        layout.addWidget(calculate_button)

        # Resultados
        self.results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout()
        
        # Resumen de carrera
        self.summary_label = QLabel("Resumen de la carrera se mostrarÃ¡ aquÃ­")
        results_layout.addWidget(self.summary_label)

        # Estrategia de carrera
        self.strategy_table = QTableWidget(0, 4)
        self.strategy_table.setHorizontalHeaderLabels(["Stint", "Compuesto", "Vueltas", "Litros"])
        self.strategy_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.strategy_table)

        self.results_group.setLayout(results_layout)
        layout.addWidget(self.results_group)

        # Estado inicial
        self.laps_radio.setChecked(True)
        self.toggle_race_type()

    def show_help(self, event):
        QMessageBox.information(self, "Ayuda sobre GestiÃ³n", "AquÃ­ va el texto explicativo sobre la gestiÃ³n de neumÃ¡ticos.")

    def toggle_race_type(self):
        self.laps_container.setEnabled(self.laps_radio.isChecked())
        self.time_container.setEnabled(self.time_radio.isChecked())

    def add_tyre_compound(self):
        compound = self.compound_input.currentText()
        life = self.tyre_life_input.value()
        item = QListWidgetItem(f"{compound} - {life} vueltas")
        item.setData(Qt.UserRole, {"compound": compound, "life": life})
        self.compound_list.addItem(item)
        self.update_compound_order()

    def update_compound_order(self):
        self.compounds = [
            self.compound_list.item(i).data(Qt.UserRole)
            for i in range(self.compound_list.count())
        ]

    def move_compound_up(self):
        current_row = self.compound_list.currentRow()
        if current_row > 0:
            item = self.compound_list.takeItem(current_row)
            self.compound_list.insertItem(current_row - 1, item)
            self.compound_list.setCurrentItem(item)
            self.update_compound_order()

    def move_compound_down(self):
        current_row = self.compound_list.currentRow()
        if current_row < self.compound_list.count() - 1:
            item = self.compound_list.takeItem(current_row)
            self.compound_list.insertItem(current_row + 1, item)
            self.compound_list.setCurrentItem(item)
            self.update_compound_order()

    def delete_compound(self):
        current_row = self.compound_list.currentRow()
        if current_row >= 0:
            self.compound_list.takeItem(current_row)
            self.update_compound_order()

    class SingleRaceTab(QWidget):
        def __init__(self):
            super().__init__()
            self.compounds = []
            self.init_ui()

        # ... (el resto de los mÃ©todos permanecen sin cambios)

    class SingleRaceTab(QWidget):
        def __init__(self):
            super().__init__()
            self.compounds = []
            self.init_ui()

    # ... (el resto de los mÃ©todos permanecen sin cambios)

    def calculate_strategy(self):
        try:
            tank_capacity = self.tank_input.value()
            consumption_per_lap = self.consumption_input.value()
            lap_time = (self.minutes_input.value() * 60 + 
                       self.seconds_input.value() + 
                       self.milliseconds_input.value() / 1000)

            # Determinar nÃºmero total de vueltas
            if self.laps_radio.isChecked():
                total_laps = self.laps_input.value()
            else:
                race_minutes = self.race_time_input.value()
                total_laps = math.ceil((race_minutes * 60) / lap_time)

            # Calcular necesidades de combustible
            total_fuel_needed = total_laps * consumption_per_lap
            extra_fuel = 2  # Litros extra de combustible
            total_fuel_with_extra = total_fuel_needed + extra_fuel
            
            # Generar resultado
            result_text_summary = f"Resumen de la carrera:\n\n"
            result_text_summary += f"Total de vueltas: {total_laps}\n"
            result_text_summary += f"Combustible total necesario: {total_fuel_with_extra:.2f}L (+2L)\n"
            
            # Calcular estrategia
            self.strategy_table.setRowCount(0)
            remaining_laps = total_laps
            current_stint = 1
            total_pit_stops = 0
            total_laps_covered = 0

            for i, compound in enumerate(self.compounds):
                stint_laps = min(remaining_laps, compound['life'])
                
                if i == 1 and remaining_laps > 0:  # Segundo stint
                    stint_laps = min(remaining_laps, compound['life'])
                    stint_laps_text = f"{stint_laps} + {remaining_laps - stint_laps}" if remaining_laps > stint_laps else str(stint_laps)
                else:
                    stint_laps_text = str(stint_laps)
                
                fuel_needed = stint_laps * consumption_per_lap
                
                if current_stint == 1:
                    # Primer stint: combustible para las vueltas efectivas mÃ¡s el extra
                    fuel_to_add = min(tank_capacity, fuel_needed + extra_fuel)
                    stint_text = "Stint 1 (Salida)"
                else:
                    # Stints siguientes: aÃ±adir el combustible necesario para este stint mÃ¡s el extra
                    fuel_to_add = min(tank_capacity, fuel_needed + extra_fuel)
                    stint_text = f"Stint {current_stint}"
                
                self.strategy_table.insertRow(self.strategy_table.rowCount())
                self.strategy_table.setItem(current_stint - 1, 0, QTableWidgetItem(stint_text))
                self.strategy_table.setItem(current_stint - 1, 1, QTableWidgetItem(compound['compound']))
                self.strategy_table.setItem(current_stint - 1, 2, QTableWidgetItem(stint_laps_text))
                self.strategy_table.setItem(current_stint - 1, 3, QTableWidgetItem(f"{fuel_to_add:.2f}"))

                remaining_laps -= stint_laps
                total_laps_covered += stint_laps
                current_stint += 1
                
                if current_stint > 2:  # Contamos las paradas a partir del segundo stint
                    total_pit_stops += 1

                if remaining_laps <= 0:
                    break

            result_text_summary += f"Paradas planificadas: {total_pit_stops}\n\n"
            
            if remaining_laps > 0:
                result_text_summary += "ADVERTENCIA: Se necesita una parada adicional para completar la carrera.\n"
                result_text_summary += f"Faltan {remaining_laps} vueltas por cubrir.\n"
            elif total_laps_covered > total_laps:
                result_text_summary += f"NOTA: La estrategia cubre {total_laps_covered} vueltas, {total_laps_covered - total_laps} mÃ¡s que la distancia de carrera.\n"
            
            self.summary_label.setText(result_text_summary)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al calcular: {str(e)}")

class SimRacingCalculator(QMainWindow):
    VERSION = "1.0"
    UPDATE_URL = "https://tu-servidor.com/updates.json"  # Esto deberÃ¡s cambiarlo

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SimRacing Calculator v{self.VERSION}")
        self.setGeometry(100, 

 100, 800, 600)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Gestor de pestaÃ±as
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Inicializar pestaÃ±as
        self.init_tabs()
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
        
        # Gestor de red para actualizaciones
        self.network_manager = QNetworkAccessManager()
    
    def init_tabs(self):
        # PestaÃ±a de carrera individual
        self.single_race_tab = SingleRaceTab()
        self.tabs.addTab(self.single_race_tab, "Carrera Individual")
        
        # PestaÃ±a de resistencia (pendiente)
        endurance_widget = QWidget()
        endurance_layout = QVBoxLayout(endurance_widget)
        endurance_layout.addWidget(QLabel("Contenido para carreras de resistencia\nPendiente de especificaciones"))
        self.tabs.addTab(endurance_widget, "Resistencia")
        
        # PestaÃ±a de actualizaciones
        self.init_updates_tab()

    def init_updates_tab(self):
        updates_widget = QWidget()
        layout = QVBoxLayout(updates_widget)
        
        # InformaciÃ³n de versiÃ³n
        version_label = QLabel(f"VersiÃ³n actual: {self.VERSION}")
        layout.addWidget(version_label)
        
        # BotÃ³n de bÃºsqueda de actualizaciones
        update_button = QPushButton("Buscar actualizaciones")
        update_button.clicked.connect(self.check_for_updates)
        layout.addWidget(update_button)
        
        # Estado de actualizaciÃ³n
        self.update_status_label = QLabel("Estado: No se han buscado actualizaciones")
        layout.addWidget(self.update_status_label)
        
        layout.addStretch()
        self.tabs.addTab(updates_widget, "Actualizaciones")
    
    def check_for_updates(self):
        self.update_status_label.setText("Buscando actualizaciones...")
        request = QNetworkRequest(QUrl(self.UPDATE_URL))
        self.network_manager.get(request).finished.connect(self.handle_update_response)
    
    def handle_update_response(self, reply):
        if reply.error():
            self.update_status_label.setText(f"Error al buscar actualizaciones: {reply.errorString()}")
            return
        
        try:
            data = json.loads(str(reply.readAll(), 'utf-8'))
            latest_version = data.get('latest_version')
            
            if latest_version > self.VERSION:
                self.update_status_label.setText(
                    f"Â¡Nueva versiÃ³n disponible! ({latest_version})\n"
                    f"DescÃ¡rgala desde: {data.get('download_url')}"
                )
            else:
                self.update_status_label.setText("EstÃ¡s utilizando la Ãºltima versiÃ³n")
        
        except json.JSONDecodeError:
            self.update_status_label.setText("Error al procesar la respuesta del servidor")
        
        reply.deleteLater()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno multiplataforma
    window = SimRacingCalculator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()