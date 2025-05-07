from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QTextEdit, QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QDateEdit, QMessageBox, QPushButton
from PySide6.QtCore import Qt, QDate, QLocale

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить задачу")
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Название задачи
        name_label = QLabel("Название задачи:")
        layout.addWidget(name_label)
        
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Введите название задачи")
        layout.addWidget(self.task_name_input)

        # Срок выполнения
        date_label = QLabel("Срок выполнения:")
        layout.addWidget(date_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("ddd, d MMMM yyyy")
        self.date_edit.setLocale(QLocale(QLocale.Russian))
        layout.addWidget(self.date_edit)

        # Описание задачи
        desc_label = QLabel("Описание задачи:")
        layout.addWidget(desc_label)
        
        self.task_description_input = QTextEdit()
        self.task_description_input.setPlaceholderText("Введите описание задачи")
        layout.addWidget(self.task_description_input)
        self.task_description_input.setFixedHeight(100)

        # Подзадачи
        subtasks_label = QLabel("Подзадачи:")
        layout.addWidget(subtasks_label)
        
        self.subtasks_input = QTextEdit()
        self.subtasks_input.setPlaceholderText("Введите подзадачи через точку с запятой (;)")
        layout.addWidget(self.subtasks_input)
        self.subtasks_input.setFixedHeight(100)

        # Приоритет
        priority_label = QLabel("Приоритет:")
        layout.addWidget(priority_label)
        
        priority_layout = QHBoxLayout()
        self.priority_group = QButtonGroup(self)
        self.priority_group.setExclusive(True)
        
        priorities = [
            ("Не задано", 0),
            ("Низкий", 1),
            ("Средний", 2),
            ("Высокий", 3)
        ]
        
        for text, priority in priorities:
            radio_btn = QRadioButton(text)
            self.priority_group.addButton(radio_btn, priority)
            priority_layout.addWidget(radio_btn)
        
        # Устанавливаем "Не задано" по умолчанию
        self.priority_group.button(0).setChecked(True)
        
        layout.addLayout(priority_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_task_name(self):
        return self.task_name_input.text()
        
    def get_priority(self):
        return self.priority_group.checkedId()
        
    def get_due_date(self):
        return self.date_edit.date().toString("ddd, d MMMM yyyy")

    def get_description(self):
        return self.task_description_input.toPlainText()

    def get_subtasks(self):
        return self.subtasks_input.toPlainText()

    def accept(self):
        if not self.task_name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым")
            return
        super().accept()

class EditListDialog(QDialog):
    def __init__(self, current_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать список")
        self.setFixedSize(400, 200)
        self.init_ui(current_name)

    def init_ui(self, current_name: str):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Поле для ввода названия
        name_label = QLabel("Название списка:")
        layout.addWidget(name_label)
        
        self.list_name_input = QLineEdit()
        self.list_name_input.setText(current_name)
        self.list_name_input.setPlaceholderText("Введите название списка")
        layout.addWidget(self.list_name_input)

        # Кнопки
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_list)
        button_layout.addWidget(self.delete_button)
        
        self.done_button = QPushButton("Готово")
        self.done_button.setObjectName("done_button")
        self.done_button.clicked.connect(self.accept)
        button_layout.addWidget(self.done_button)
        
        layout.addLayout(button_layout)

    def get_list_name(self):
        return self.list_name_input.text()

    def delete_list(self):
        self.done(2)  # Специальный код для удаления списка
    
