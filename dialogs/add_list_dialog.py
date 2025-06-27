from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class AddListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить список")
        self.setFixedSize(self.sizeHint())
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.name_label = QLabel("Название списка:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название списка")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        
        self.done_button = QPushButton("Готово")
        self.done_button.clicked.connect(self.accept)
        self.done_button.setEnabled(False)

        self.name_input.textChanged.connect(self.check_text)

        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.done_button = QPushButton("Готово")
        self.done_button.setObjectName("done_button")
        self.done_button.clicked.connect(self.accept)
        button_layout.addWidget(self.done_button)
        
        layout.addLayout(button_layout)

        for btn in self.findChildren(QPushButton):
            btn.setCursor(Qt.PointingHandCursor)

    def check_text(self):
        self.done_button.setEnabled(bool(self.name_input.text().strip()))

    def get_list_name(self):
        return self.name_input.text().strip()

    def accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название списка не может быть пустым")
            return
        super().accept() 