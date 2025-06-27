from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QTextEdit, QHBoxLayout, QRadioButton, QButtonGroup, QLabel, QDateEdit, QMessageBox, QPushButton, QComboBox
from PySide6.QtCore import Qt, QDate
import json

class AddTaskDialog(QDialog):
    def __init__(self, parent=None, from_all_tasks=False, task_data=None, on_delete=None):
        super().__init__(parent)
        self.from_all_tasks = from_all_tasks
        self.task_data = task_data
        self.on_delete = on_delete
        if self.task_data:
            self.setWindowTitle("Редактировать задачу")
        else:
            self.setWindowTitle("Добавить задачу")

        self.setFixedSize(self.sizeHint())
        self.init_ui()

        if self.task_data:
            # Название задачи
            self.task_name_input.setText(self.task_data.get('task_name', ''))
            # Описание
            self.task_description_input.setText(self.task_data.get('task_description', ''))
            # Дата выполнения
            date_str = self.task_data.get('task_due_date', '')
            if date_str:
                date = QDate.fromString(date_str, "ddd, d MMMM yyyy")
                if date.isValid():
                    self.date_edit.setDate(date)
            # Подзадачи
            subtasks = self.task_data.get('task_subtasks', [])
            if isinstance(subtasks, list):
                subtasks_str = "; ".join([s.get('subtask_name', '') for s in subtasks if s.get('subtask_name', '')])
            else:
                subtasks_str = str(subtasks)
            self.subtasks_input.setText(subtasks_str)
            # Приоритет
            priority = self.task_data.get('task_priority', 0)
            if self.priority_group.button(priority):
                self.priority_group.button(priority).setChecked(True)
            # Активировать кнопку сохранения, если есть название
            self.save_button.setEnabled(bool(self.task_name_input.text().strip()))

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        if self.from_all_tasks:
            list_label = QLabel("Выберите список:")
            list_label.setObjectName("dialog_label")
            layout.addWidget(list_label)
            
            self.list_select = QComboBox()
            self.list_select.setObjectName("priority_sort_select")
            self.list_select.setMinimumHeight(40)
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
        self.task_name_input.setMinimumHeight(40)
        layout.addWidget(self.task_name_input)

        # Описание
        description_label = QLabel("Описание:")
        description_label.setObjectName("dialog_label")
        layout.addWidget(description_label)
        
        self.task_description_input = QTextEdit()
        self.task_description_input.setPlaceholderText("Введите описание задачи")
        self.task_description_input.setMinimumHeight(120)
        layout.addWidget(self.task_description_input)

        # Дата выполнения
        date_label = QLabel("Дата выполнения:")
        date_label.setObjectName("dialog_label")
        layout.addWidget(date_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumHeight(40)
        layout.addWidget(self.date_edit)

        # Подзадачи
        subtasks_label = QLabel("Подзадачи:")
        subtasks_label.setObjectName("dialog_label")
        layout.addWidget(subtasks_label)
        
        self.subtasks_input = QTextEdit()
        self.subtasks_input.setPlaceholderText("Введите подзадачи через точку с запятой (;)")
        self.subtasks_input.setMinimumHeight(120)
        layout.addWidget(self.subtasks_input)

        # Приоритет
        priority_label = QLabel("Приоритет:")
        priority_label.setObjectName("dialog_label")
        layout.addWidget(priority_label)
        
        priority_layout = QHBoxLayout()
        priority_layout.setSpacing(20)
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
            radio_btn.setMinimumHeight(24)
            self.priority_group.addButton(radio_btn, priority)
            priority_layout.addWidget(radio_btn)
        
        self.priority_group.button(0).setChecked(True)
        
        layout.addLayout(priority_layout)

        layout.addStretch()

        if not self.task_data:
            self.button_box = QDialogButtonBox(self)
            self.cancel_button = self.button_box.addButton("Отмена", QDialogButtonBox.RejectRole)
            self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.AcceptRole)
            self.cancel_button.setObjectName('cancel_button')
            self.button_box.rejected.connect(self.reject)
            self.button_box.accepted.connect(self.accept)
            layout.addWidget(self.button_box)
            self.button_box.setStyleSheet("""
            margin-top: '12px';
""")
        else:
            self.button_box = QDialogButtonBox(self)
            self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.AcceptRole)
            self.delete_button = self.button_box.addButton("Удалить задачу", QDialogButtonBox.RejectRole)
            self.save_button.setStyleSheet("""
                    background-color: #6C946D;
                    border-radius: 6px;
                    padding: 8px 16px;
                    color: white;
                    font-size: 14px;
                    font-weight: 500;
                    min-width: 120px;
                    max-width: 120px;
                    min-height: 20px;
                    max-height: 20px;
""")
            self.delete_button.setStyleSheet("""
                    background-color: #FF6B6B;
                    border-radius: 6px;
                    padding: 8px 16px;
                    color: white;
                    font-size: 14px;
                    font-weight: 500;
                    min-width: 120px;
                    max-width: 120px;
                    min-height: 20px;
                    max-height: 20px;
            """)
            self.button_box.rejected.connect(self.handle_delete)
            self.button_box.accepted.connect(self.accept)
            self.button_box.setStyleSheet("""
            margin-top: '12px';
""")
            layout.addWidget(self.button_box)


    def on_task_name_changed(self):
        self.save_button.setEnabled(bool(self.task_name_input.text().strip()))

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
        return 0

    def accept(self):
        if not self.task_name_input.text().strip():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Ошибка")
            msg.setText("Название задачи не может быть пустым")
            ok_button = msg.addButton(QMessageBox.Ok)
            ok_button.setStyleSheet("background-color: #6C946D; color: #F3F2F3; border-radius: 8px; padding: 8px 16px; font-size: 16px; font-weight: 500; min-width: 100px;")
            msg.exec()
            return
        super().accept()

    def handle_delete(self):
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Warning)
        reply.setWindowTitle("Подтверждение удаления")
        reply.setText("Действительно удалить задачу?")
        delete_btn = reply.addButton("Удалить", QMessageBox.AcceptRole)
        cancel_btn = reply.addButton("Отмена", QMessageBox.RejectRole)
        delete_btn.setStyleSheet("background-color: #FF6B6B; color: white; border-radius: 8px; padding: 8px 16px; font-size: 16px; font-weight: 500; min-width: 100px;")
        cancel_btn.setStyleSheet("background-color: #B1CCBB; color: #353028; border-radius: 8px; padding: 8px 16px; font-size: 16px; font-weight: 500; min-width: 100px;")
        reply.exec()
        if reply.clickedButton() == delete_btn:
            if self.on_delete:
                self.on_delete()
            self.reject() 