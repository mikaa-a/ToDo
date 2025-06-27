from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class EditListDialog(QDialog):
    def __init__(self, current_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать список")
        self.setFixedSize(self.sizeHint())
        self.init_ui(current_name)

    def init_ui(self, current_name: str):
        layout = QVBoxLayout()
        self.setLayout(layout)

        name_label = QLabel("Название списка:")
        layout.addWidget(name_label)
        
        self.list_name_input = QLineEdit()
        self.list_name_input.setText(current_name)
        self.list_name_input.setPlaceholderText("Введите название списка")
        layout.addWidget(self.list_name_input)

        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_list)
        button_layout.addWidget(self.delete_button)
        
        self.done_button = QPushButton("Готово")
        self.done_button.setObjectName("done_button")
        self.done_button.clicked.connect(self.on_done_clicked)
        button_layout.addWidget(self.done_button)
        
        layout.addLayout(button_layout)

        for btn in self.findChildren(QPushButton):
            btn.setCursor(Qt.PointingHandCursor)

    def get_list_name(self):
        return self.list_name_input.text()

    def delete_list(self):
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Warning)
        reply.setWindowTitle("Подтверждение удаления")
        reply.setText("Действительно удалить список?")
        delete_btn = reply.addButton("Удалить", QMessageBox.AcceptRole)
        cancel_btn = reply.addButton("Отмена", QMessageBox.RejectRole)
        delete_btn.setStyleSheet("background-color: #FF6B6B; color: white; border-radius: 8px; padding: 8px 16px; font-size: 16px; font-weight: 500; min-width: 100px;")
        cancel_btn.setStyleSheet("background-color: #B1CCBB; color: #353028; border-radius: 8px; padding: 8px 16px; font-size: 16px; font-weight: 500; min-width: 100px;")
        reply.exec()
        if reply.clickedButton() == delete_btn:
            self.done(2)

    def on_done_clicked(self):
        if not self.list_name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название списка не может быть пустым")
            return
        self.accept()
