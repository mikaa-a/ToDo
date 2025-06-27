import json
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame, QSizePolicy, QLayout, QSpacerItem
from PySide6.QtCore import Qt, QDate
from dialogs.add_task_dialog import AddTaskDialog 

class TaskCard(QWidget):
    def __init__(self, text: str, date: str, priority: str, description: str, sub_tasks: str, task_id: int, parent=None):
        super().__init__()
        self.task_id = task_id
        self.parent = parent
        self.setObjectName("task_card_widget")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumWidth(0)

        self.container = QFrame()
        self.container.setObjectName("task_card")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.container.setMinimumWidth(0)
        self.container.setStyleSheet("background-color: #B1CCBB; border-radius: 16px;")

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(6)

        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("task_checkbox")
        self.checkbox.clicked.connect(self.handle_task_click)
        checkbox_container = QWidget()
        checkbox_container.setObjectName("checkbox_container")
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(6, 4, 0, 0)
        checkbox_layout.setSpacing(0)
        checkbox_layout.addWidget(self.checkbox, alignment=Qt.AlignCenter)
        self.top_layout.addWidget(checkbox_container, alignment=Qt.AlignVCenter)

        self.task_name = QLabel(text)
        self.task_name.setObjectName("task_name")
        self.task_name.setWordWrap(True)
        self.task_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.task_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.top_layout.addWidget(self.task_name)

        self.top_layout.addStretch()

        self.top_info = QLabel(f"{self.format_date(date)}  •  {self.get_priority_text(priority)}")
        self.top_info.setObjectName("task_top_info")
        self.top_info.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.top_layout.addWidget(self.top_info)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addItem(QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.description_label = QLabel("Описание:")
        self.description_label.setObjectName("description_label")
        self.description_label.setWordWrap(True)
        self.main_layout.addWidget(self.description_label)

        self.task_description = QLabel(description)
        self.task_description.setObjectName("task_description")
        self.task_description.setWordWrap(True)
        self.task_description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.main_layout.addWidget(self.task_description)
        self.description_label.setVisible(bool(description))

        self.main_layout.addItem(QSpacerItem(24, 12, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.subtasks_label = QLabel("Подзадачи:")
        self.subtasks_label.setObjectName("subtasks_label")
        self.main_layout.addWidget(self.subtasks_label)

        self.subtasks_scroll = QScrollArea()
        self.subtasks_scroll.setObjectName("subtasks_scroll")
        self.subtasks_scroll.setWidgetResizable(True)
        self.subtasks_scroll.setFixedHeight(120)
        self.subtasks_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.subtasks_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.subtasks_container = QWidget()
        self.subtasks_container.setObjectName("subtasks_container")
        self.subtasks_layout = QVBoxLayout(self.subtasks_container)
        self.subtasks_layout.setSpacing(4)
        self.subtasks_layout.setContentsMargins(5, 8, 5, 8)
        self.subtasks_scroll.setWidget(self.subtasks_container)
        self.main_layout.addWidget(self.subtasks_scroll)

        if sub_tasks:
            subtasks_list = [subtask.strip() for subtask in sub_tasks.split(';') if subtask.strip()]
            for subtask_text in subtasks_list:
                subtask_widget = QWidget()
                subtask_widget.setFixedHeight(20)
                subtask_layout = QHBoxLayout(subtask_widget)
                subtask_layout.setContentsMargins(0, 0, 0, 0)
                subtask_layout.setSpacing(4)

                subtask = SubtaskWidget(subtask_text)
                subtask.checkbox.clicked.connect(lambda checked, w=subtask: self.handle_subtask_click(checked, w))
                subtask_layout.addWidget(subtask)
                self.subtasks_layout.addWidget(subtask_widget)
        else:
            self.subtasks_label.setVisible(False)
            self.subtasks_scroll.setVisible(False)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setStyleSheet("background-color: #6C946D; border: none; border-radius: 10px; color: #F3F2F3; font-size: 14px; font-weight: 400; padding: 4px 12px; min-width: 108px; max-width: 108px; min-height: 20px; max-height: 20px;")
        self.edit_button.clicked.connect(self.edit_task)
        self.main_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)

        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

    def get_priority_text(self, priority) -> str:
        priority_map = {
            1: "Низкий приоритет",
            2: "Средний приоритет",
            3: "Высокий приоритет",
            0: "Приоритет не задан",
            "1": "Низкий приоритет",
            "2": "Средний приоритет",
            "3": "Высокий приоритет",
            "0": "Приоритет не задан"
        }
        return priority_map.get(priority, "Приоритет не задан")

    def format_date(self, date_str: str) -> str:
        if not date_str:
            return "Дата не задана"
        date = QDate.fromString(date_str, "ddd, d MMMM yyyy")
        if not date.isValid():
            return "Дата не задана"
        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        return f"{date.day()} {months[date.month()]} {date.year()}"

    def edit_task(self):
        # Собираем данные задачи
        task_data = {
            'task_name': self.task_name.text(),
            'task_description': self.task_description.text(),
            'task_due_date': self.top_info.text().split(' • ')[0],
            'task_priority': {"Низкий приоритет": 1, "Средний приоритет": 2, "Высокий приоритет": 3, "Приоритет не задан": 0}.get(self.top_info.text().split(' • ')[1].strip(), 0),
            'task_subtasks': [
                {'subtask_name': self.subtasks_layout.itemAt(i).widget().findChild(QLabel).text()}
                for i in range(self.subtasks_layout.count())
                if self.subtasks_layout.itemAt(i).widget()
            ]
        }
        def on_delete():
            self.delete_task()
        dialog = AddTaskDialog(self, task_data=task_data, on_delete=on_delete)
        if dialog.exec() == QDialog.Accepted:
            self.task_name.setText(dialog.get_task_name())
            self.task_description.setText(dialog.get_description())
            self.top_info.setText(f"{self.format_date(dialog.get_due_date())} • {self.get_priority_text(dialog.get_priority())}")
            self.description_label.setVisible(bool(dialog.get_description()))

            for i in reversed(range(self.subtasks_layout.count())):
                self.subtasks_layout.itemAt(i).widget().deleteLater()
            subtasks = dialog.get_subtasks()
            if subtasks:
                subtasks_list = [subtask.strip() for subtask in subtasks.split(';') if subtask.strip()]
                for subtask_text in subtasks_list:
                    subtask_widget = QWidget()
                    subtask_widget.setFixedHeight(20)
                    subtask_layout = QHBoxLayout(subtask_widget)
                    subtask_layout.setContentsMargins(0, 0, 0, 0)
                    subtask_layout.setSpacing(4)
                    subtask = SubtaskWidget(subtask_text)
                    subtask.checkbox.clicked.connect(lambda checked, w=subtask: self.handle_subtask_click(checked, w))
                    subtask_layout.addWidget(subtask)
                    self.subtasks_layout.addWidget(subtask_widget)
                self.subtasks_label.setVisible(True)
                self.subtasks_scroll.setVisible(True)
            else:
                self.subtasks_label.setVisible(False)
                self.subtasks_scroll.setVisible(False)

            self._update_json(dialog)

    def delete_task(self):
        # Удаление из layout
        layout = getattr(self.parent, 'tasks_layout', None)
        all_tasks_layout = getattr(self.parent, 'all_tasks_layout', None)
        if layout:
            layout.removeWidget(self)
            self.setParent(None)
            self.deleteLater()
        if all_tasks_layout:
            all_tasks_layout.removeWidget(self)
            self.setParent(None)
            self.deleteLater()
        # Удаление из data.json
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            for task_list in data:
                for i, task in enumerate(task_list['tasks']):
                    if task['id'] == self.task_id:
                        del task_list['tasks'][i]
                        break
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")

    def handle_task_click(self, checked):
        self.task_name.setStyleSheet("text-decoration: line-through; color: #666666;" if checked else "")
        layout = getattr(self.parent, 'tasks_layout', None)
        all_tasks_layout = getattr(self.parent, 'all_tasks_layout', None)
        if layout:
            # Перемещаем задачу в самый низ (если выполнена) или вверх (если не выполнена)
            layout.removeWidget(self)
            count = layout.count()
            if checked:
                layout.insertWidget(count, self)
            else:
                layout.insertWidget(0, self)
        if all_tasks_layout:
            all_tasks_layout.removeWidget(self)
            count = all_tasks_layout.count()
            if checked:
                all_tasks_layout.insertWidget(count, self)
            else:
                all_tasks_layout.insertWidget(0, self)

        for i in range(self.subtasks_layout.count()):
            widget = self.subtasks_layout.itemAt(i).widget()
            if widget:
                checkbox = widget.findChild(QCheckBox)
                label = widget.findChild(QLabel)
                if checkbox and label:
                    checkbox.setChecked(checked)
                    label.setStyleSheet("text-decoration: line-through; color: #666666;" if checked else "")

        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            task_list = data[0]
            for task in task_list['tasks']:
                if task['id'] == self.task_id:
                    task['task_is_done'] = checked
                    for subtask in task['task_subtasks']:
                        subtask['is_completed'] = checked
                    break
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении состояния задачи: {e}")
        # После изменения статуса задачи пересобираем список, если это страница конкретного списка
        if (
            hasattr(self.parent, 'current_list_card') and self.parent.current_list_card is not None
            and hasattr(self.parent, 'stacked_widget') and self.parent.stacked_widget.currentIndex() == 1
        ):
            self.parent.open_list(self.parent.current_list_card)

    def handle_subtask_click(self, checked, widget):
        widget.update_style()
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            task_list = data[0]
            for task in task_list['tasks']:
                if task['id'] == self.task_id:
                    subtask_text = widget.label.text()
                    subtasks = task['task_subtasks']
                    for subtask in subtasks:
                        if subtask['subtask_name'] == subtask_text:
                            subtask['is_completed'] = checked
                            subtasks.remove(subtask)
                            subtasks.insert(-1 if checked else 0, subtask)
                            break
                    task['task_subtasks'] = subtasks
                    break
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении состояния подзадачи: {e}")

    def _update_json(self, dialog):
        """Обновляет данные задачи в JSON."""
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            task_list = data[0]
            for task in task_list['tasks']:
                if task['id'] == self.task_id:
                    task.update({
                        'task_name': dialog.get_task_name(),
                        'task_description': dialog.get_description(),
                        'task_priority': dialog.get_priority(),
                        'task_due_date': dialog.get_due_date(),
                        'task_subtasks': [
                            {"id": i + 1, "subtask_name": subtask.strip()}
                            for i, subtask in enumerate(dialog.get_subtasks().split(';') if dialog.get_subtasks() else [])
                            if subtask.strip()
                        ]
                    })
                    break
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при обновлении задачи: {e}")

class SubtaskWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setObjectName("subtask_widget")
        self.setFixedHeight(20)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("subtask_checkbox")
        layout.addWidget(self.checkbox, 0, Qt.AlignVCenter)

        self.label = QLabel(text)
        self.label.setObjectName("subtask_label")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.label, 1)

        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.checkbox.setChecked(not self.checkbox.isChecked())
        self.update_style()
        super().mousePressEvent(event)

    def update_style(self):
        self.label.setStyleSheet(
            "font-size: 18px; color: #666666; font-weight: 400; padding: 0px; margin-top: 0px; line-height: 18px; text-decoration: line-through;"
            if self.checkbox.isChecked() else
            "font-size: 18px; color: #353028; font-weight: 400; padding: 0px; margin-top: 0px; line-height: 18px;"
        )