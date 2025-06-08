from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QTextEdit, QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QDateEdit, QMessageBox, QPushButton, QComboBox
from PySide6.QtCore import Qt, QDate, QLocale
import json

class AddTaskDialog(QDialog):
    def __init__(self, parent=None, from_all_tasks=False):
        super().__init__(parent)
        self.from_all_tasks = from_all_tasks
        self.setWindowTitle("Добавить задачу")

        self.setMinimumSize(500, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Увеличиваем расстояние между элементами
        layout.setContentsMargins(20, 20, 20, 20)  # Добавляем отступы
        self.setLayout(layout)

        # Добавляем выбор списка, если диалог открыт из "Все задачи"
        if self.from_all_tasks:
            list_label = QLabel("Выберите список:")
            list_label.setObjectName("dialog_label")
            layout.addWidget(list_label)
            
            self.list_select = QComboBox()
            self.list_select.setObjectName("priority_sort_select")
            self.list_select.setMinimumHeight(40)  # Увеличиваем высоту комбо бокса
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for list_item in data:
                        self.list_select.addItem(list_item['list_name'])
            except Exception as e:
                print(f"Ошибка при загрузке списков: {e}")
            layout.addWidget(self.list_select)

        # Название задачи
        name_label = QLabel("Название задачи:")
        name_label.setObjectName("dialog_label")
        layout.addWidget(name_label)
        
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Введите название задачи")
        self.task_name_input.setMinimumHeight(40)  # Увеличиваем высоту поля ввода
        layout.addWidget(self.task_name_input)

        # Описание
        description_label = QLabel("Описание:")
        description_label.setObjectName("dialog_label")
        layout.addWidget(description_label)
        
        self.task_description_input = QTextEdit()
        self.task_description_input.setPlaceholderText("Введите описание задачи")
        self.task_description_input.setMinimumHeight(120)  # Увеличиваем высоту поля описания
        layout.addWidget(self.task_description_input)

        # Дата выполнения
        date_label = QLabel("Дата выполнения:")
        date_label.setObjectName("dialog_label")
        layout.addWidget(date_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumHeight(40)  # Увеличиваем высоту поля даты
        layout.addWidget(self.date_edit)

        # Подзадачи
        subtasks_label = QLabel("Подзадачи:")
        subtasks_label.setObjectName("dialog_label")
        layout.addWidget(subtasks_label)
        
        self.subtasks_input = QTextEdit()
        self.subtasks_input.setPlaceholderText("Введите подзадачи через точку с запятой (;)")
        self.subtasks_input.setMinimumHeight(120)  # Увеличиваем высоту поля подзадач
        layout.addWidget(self.subtasks_input)

        # Приоритет
        priority_label = QLabel("Приоритет:")
        priority_label.setObjectName("dialog_label")
        layout.addWidget(priority_label)
        
        priority_layout = QHBoxLayout()
        priority_layout.setSpacing(20)  # Увеличиваем расстояние между радио кнопками
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
            radio_btn.setMinimumHeight(30)  # Увеличиваем высоту радио кнопок
            self.priority_group.addButton(radio_btn, priority)
            priority_layout.addWidget(radio_btn)
        
        # Устанавливаем "Не задано" по умолчанию
        self.priority_group.button(0).setChecked(True)
        
        layout.addLayout(priority_layout)

        # Добавляем растягивающийся элемент перед кнопками
        layout.addStretch()

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

    def get_selected_list_index(self):
        if self.from_all_tasks:
            return self.list_select.currentIndex()
        return 0  # Возвращаем 0, если диалог открыт не из "Все задачи"

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
    
