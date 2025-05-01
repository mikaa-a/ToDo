import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy, QVBoxLayout, QWidget
from PySide6.QtCore import QFile, Qt
from ui_mainwindow import Ui_Form

class TaskCard(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName("task_card")
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setMinimumHeight(40)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set fixed window size
        self.setFixedSize(1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.ui = Ui_Form()
        self.ui.setupUi(self.central_widget)

        self.MARGIN = 20
        self.ui.content.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)

        self.ui.tasks_layout.setAlignment(Qt.AlignTop)
        self.ui.tasks_layout.setSpacing(10)

        self.ui.add_task_btn.clicked.connect(self.add_new_task)

        # Set initial page
        self.ui.content.setCurrentIndex(1)  # Show list_page at startup for testing

    def add_task_to_layout(self, layout, text: str):
        task = TaskCard(text)
        layout.addWidget(task)

    def add_new_task(self):
        self.add_task_to_layout(self.ui.tasks_layout, "Новая задача " + str(self.ui.tasks_layout.count() + 1))

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