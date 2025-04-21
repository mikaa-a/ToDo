import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import QFile, Qt
from ui_mainwindow import Ui_Form

class TaskCard(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setObjectName("task_card")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.tasks_layout.setAlignment(Qt.AlignTop)

        self.ui.add_task_btn.clicked.connect(self.add_new_task)

    def add_task_to_layout(self, layout, text: str):
        task = TaskCard(text)
        layout.addWidget(task)

    def add_new_task(self):
        self.add_task_to_layout(self.ui.tasks_layout, "Поцеловать зайчика")

def load_stylesheet(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("Ошибка при загрузке стилей:", e)
        return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet = load_stylesheet("styles.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
