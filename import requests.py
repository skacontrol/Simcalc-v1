import requests
import base64
from datetime import datetime
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

class GitHubUpdater:
    def __init__(self, token: str, owner: str, repo: str):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.owner = owner
        self.repo = repo

    def get_file_content(self, path: str, branch: str = "main"):
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{path}"
        params = {"ref": branch}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content, data["sha"]
        return None

    def update_file(self, path: str, content: str, message: str, branch: str = "main") -> bool:
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{path}"
        existing_content = self.get_file_content(path, branch)
        sha = existing_content[1] if existing_content else None
        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }
        if sha:
            data["sha"] = sha

        response = requests.put(url, headers=self.headers, json=data)
        if response.status_code not in (200, 201):
            print(f"Error: {response.json()}")
            return False
        return True

class UpdateWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.files_to_update = []
        self.updater = GitHubUpdater(os.getenv("GITHUB_TOKEN"), "skacontrol", "Simcalc-v1")

    def initUI(self):
        self.setWindowTitle("ActualizaciÃ³n de Archivos en GitHub")
        self.setGeometry(100, 100, 500, 400)

        self.select_folder_button = QtWidgets.QPushButton("Seleccionar carpeta", self)
        self.select_folder_button.setGeometry(30, 30, 200, 30)
        self.select_folder_button.clicked.connect(self.select_folder)

        self.upload_button = QtWidgets.QPushButton("Subir archivos", self)
        self.upload_button.setGeometry(250, 30, 200, 30)
        self.upload_button.clicked.connect(self.update_files)
        self.upload_button.setEnabled(False)

        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setGeometry(30, 80, 440, 25)

        self.status_label = QtWidgets.QLabel("Seleccione una carpeta para comenzar.", self)
        self.status_label.setGeometry(30, 120, 440, 20)

        self.file_list = QtWidgets.QListWidget(self)
        self.file_list.setGeometry(30, 150, 440, 180)

        self.close_button = QtWidgets.QPushButton("Salir", self)
        self.close_button.setGeometry(200, 350, 100, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setEnabled(False)

        self.show()

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder_path:
            self.files_to_update = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
            self.file_list.clear()
            self.file_list.addItems([os.path.basename(f) for f in self.files_to_update])
            self.upload_button.setEnabled(True)
            self.status_label.setText(f"Carpeta seleccionada: {folder_path}")

    def update_files(self):
        if not self.files_to_update:
            self.status_label.setText("No hay archivos para actualizar.")
            return

        self.progress_bar.setMaximum(len(self.files_to_update))
        updated_files = []

        for index, file_path in enumerate(self.files_to_update):
            with open(file_path, "r") as f:
                content = f.read()

            file_name = os.path.basename(file_path)
            success = self.updater.update_file(
                path=file_name,
                content=content,
                message="ActualizaciÃ³n automÃ¡tica de archivo"
            )

            if success:
                updated_files.append(file_name)
                self.file_list.addItem(f"Actualizado: {file_name}")
            else:
                self.file_list.addItem(f"Error: {file_name}")

            self.progress_bar.setValue(index + 1)

        if updated_files:
            self.status_label.setText("ActualizaciÃ³n completada.")
        else:
            self.status_label.setText("No hay archivos para actualizar.")

        self.close_button.setEnabled(True)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = UpdateWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
