from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class AddListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить список")
        self.setMinimumWidth(300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Добавляем поле ввода
        self.name_label = QLabel("Название списка:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название списка")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Добавляем кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        
        self.done_button = QPushButton("Готово")
        self.done_button.clicked.connect(self.accept)
        self.done_button.setEnabled(False)  # Изначально кнопка неактивна

        # Подключаем проверку текста
        self.name_input.textChanged.connect(self.check_text)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.done_button)
        layout.addLayout(button_layout)

    def check_text(self):
        # Активируем кнопку "Готово" только если есть текст
        self.done_button.setEnabled(bool(self.name_input.text().strip()))

    def get_list_name(self):
        return self.name_input.text().strip() 