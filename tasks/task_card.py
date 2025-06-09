import json
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame, QSizePolicy, QLayout
from PySide6.QtCore import Qt, QDate
from dialogs.dialog import AddTaskDialog

class TaskCard(QWidget):
    def __init__(self, text: str, date: str, priority: str, description: str, sub_tasks: str, task_id: int, parent=None):
        super().__init__()
        self.task_id = task_id
        self.parent = parent
        
        # Устанавливаем политику размеров для карточки
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumWidth(0)  # Позволяем карточке сжиматься
        
        # Создаем контейнер для стилей
        self.container = QFrame()
        self.container.setObjectName("task_card")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.container.setMinimumWidth(0)
        self.container.setStyleSheet("""
            QFrame#task_card {
                background-color: #B1CCBB;
                border-radius: 12px;
                padding: 12px;
                min-width: 0;  /* Позволяет контейнеру сжиматься */
            }
            QLabel#task_name, QLabel#task_description, QLabel#description_label, QLabel#subtasks_label, QLabel#task_top_info {
                background-color: transparent;
            }
            QPushButton#edit_button {
                background-color: #6C946D;
                border: none;
                border-radius: 8px;
                color: #F3F2F3;
                font-size: 16px;
                font-weight: 400;
                padding: 4px 12px;
                min-width: 120px;
                max-width: 120px;
                min-height: 32px;
                max-height: 32px;
            }
            QPushButton#edit_button:hover {
                background-color: #8AB38B;
            }
            QPushButton#edit_button:pressed {
                background-color: #4A7C5B;
                color: #F3F2F3;
            }
            QCheckBox#task_checkbox {
                background-color: transparent;
                spacing: 0px;
                margin: 0px;
                padding: 0px;
            }
            QCheckBox#task_checkbox::indicator {
                width: 24px;
                height: 24px;
                border: 1px solid #353028;
                border-radius: 4px;
                margin: 0px;
                padding: 0px;
            }
            QCheckBox#task_checkbox::indicator:checked {
                background-color: #6C946D;
                border: none;
                image: url(check.png);
            }
            QCheckBox#task_checkbox::indicator:hover {
                border-color: #8AB38B;
            }
            QCheckBox#task_checkbox::indicator:checked:hover {
                background-color: #8AB38B;
            }
            QWidget#checkbox_container {
                background-color: transparent;
            }
        """)
        
        # Основной layout для контейнера
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(6)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        # Верхняя часть с названием, датой и приоритетом
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(6)
        
        # Чекбокс и название задачи
        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("task_checkbox")
        self.checkbox.setFixedSize(24, 24)  # Уменьшаем размер чекбокса
        self.checkbox.setContentsMargins(0, 0, 0, 0)
        self.checkbox.clicked.connect(self.handle_task_click)
        checkbox_container = QWidget()
        checkbox_container.setObjectName("checkbox_container")
        checkbox_container.setFixedSize(32, 32)  # Уменьшаем размер контейнера
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(4, 4, 4, 4)  # Уменьшаем отступы
        checkbox_layout.setSpacing(0)
        checkbox_layout.addWidget(self.checkbox, alignment=Qt.AlignCenter)
        self.top_layout.addWidget(checkbox_container, alignment=Qt.AlignVCenter)  # Выравниваем по вертикали
        
        self.task_name = QLabel(text)
        self.task_name.setObjectName("task_name")
        self.task_name.setWordWrap(True)
        self.task_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.task_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Выравниваем текст по вертикали
        self.top_layout.addWidget(self.task_name)
        
        # Добавляем растягивающийся элемент
        self.top_layout.addStretch()
        
        # Дата и приоритет
        self.top_info = QLabel(f"{self.format_date(date)} • {self.get_priority_text(priority)}")
        self.top_info.setObjectName("task_top_info")
        self.top_info.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.top_layout.addWidget(self.top_info)
        
        self.main_layout.addLayout(self.top_layout)

        # Описание
        self.description_label = QLabel("Описание:")
        self.description_label.setObjectName("description_label")
        self.description_label.setWordWrap(True)
        self.main_layout.addWidget(self.description_label)

        if not description:
            self.description_label.setVisible(False)
        else:
            self.description_label.setVisible(True)

        self.task_description = QLabel(description)
        self.task_description.setObjectName("task_description")
        self.task_description.setWordWrap(True)  # Разрешаем перенос текста
        self.task_description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.main_layout.addWidget(self.task_description)

        # Подзадачи
        self.subtasks_label = QLabel("Подзадачи:")
        self.subtasks_label.setObjectName("subtasks_label")
        self.main_layout.addWidget(self.subtasks_label)

        # Создаем контейнер для подзадач с прокруткой
        self.subtasks_scroll = QScrollArea()
        self.subtasks_scroll.setWidgetResizable(True)
        self.subtasks_scroll.setMaximumHeight(120)  # Уменьшаем максимальную высоту
        self.subtasks_scroll.setMinimumHeight(0)
        self.subtasks_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.subtasks_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем вертикальную прокрутку
        self.subtasks_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
                
        self.subtasks_container = QWidget()
        self.subtasks_container.setStyleSheet("""
            QWidget {
                background-color: #B1CCBB;
                border-radius: 8px;
            }
            QLabel {
                background-color: transparent;
            }
        """)
        self.subtasks_layout = QVBoxLayout(self.subtasks_container)
        self.subtasks_layout.setSpacing(5)
        self.subtasks_layout.setContentsMargins(10, 10, 10, 10)
        self.subtasks_scroll.setWidget(self.subtasks_container)
        self.main_layout.addWidget(self.subtasks_scroll)

        # Добавляем подзадачи с чекбоксами
        if sub_tasks:
            subtasks_list = [subtask.strip() for subtask in sub_tasks.split(';') if subtask.strip()]
            
            # Вычисляем необходимую высоту для контейнера
            total_height = len(subtasks_list) * 32  # Высота одной подзадачи (32px)
            self.subtasks_scroll.setFixedHeight(total_height + 20)  # Добавляем отступы
                
            for i, subtask in enumerate(subtasks_list, 1):
                subtask_widget = QWidget()
                subtask_widget.setFixedHeight(32)  # Фиксированная высота контейнера
                subtask_layout = QHBoxLayout(subtask_widget)
                subtask_layout.setContentsMargins(0, 0, 0, 0)
                subtask_layout.setSpacing(8)
                
                subtask = SubtaskWidget(subtask)
                subtask.checkbox.clicked.connect(lambda checked, w=subtask: self.handle_subtask_click(checked, w))
                subtask_layout.addWidget(subtask)
                
                self.subtasks_layout.addWidget(subtask_widget)
        else:
            self.subtasks_label.setVisible(False)
            self.subtasks_scroll.setVisible(False)

        # Кнопка редактирования
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.clicked.connect(self.edit_task)
        self.main_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)

        # Устанавливаем layout для основного виджета
        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

    def get_priority_text(self, priority: int):
        match priority:
            case 1:
                return "Низкий приоритет"
            case 2:
                return "Средний приоритет"
            case 3:
                return "Высокий приоритет   "
            case 0:
                return "Приоритет не задан"
            case _:
                return "Приоритет не задан"

    def format_date(self, date_str: str) -> str:
        if not date_str:
            return "Дата не задана"
        
        try:
            print(f"Полученная дата: {date_str}")
            # Преобразуем строку даты в QDate
            date = QDate.fromString(date_str, "ddd, d MMMM yyyy")
            if not date.isValid():
                return "Дата не задана"
                
            months = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                5: "мая", 6: "июня", 7: "июля", 8: "августа",
                9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
            }
            return f"{date.day()} {months[date.month()]} {date.year()}"
        except Exception as e:
            print(f"Ошибка при форматировании даты: {e}")
            return "Дата не задана"

    def edit_task(self):
        dialog = AddTaskDialog(self)
        dialog.setWindowTitle("Редактировать задачу")
        
        # Заполняем поля текущими данными
        dialog.task_name_input.setText(self.task_name.text())
        dialog.task_description_input.setText(self.task_description.text())
        
        # Устанавливаем дату
        date = QDate.fromString(self.top_info.text().split(' • ')[0], "d MMMM yyyy")
        if date.isValid():
            dialog.date_edit.setDate(self.format_date(date))
            
        # Устанавливаем приоритет
        priority_text = self.top_info.text().split(' • ')[1].strip()
        priority_map = {
            "Низкий приоритет": 1,
            "Средний приоритет": 2,
            "Высокий приоритет": 3,
            "Приоритет не задан": 0
        }
        dialog.priority_group.button(priority_map.get(priority_text, 0)).setChecked(True)
        
        # Устанавливаем подзадачи
        subtasks = []
        for i in range(self.subtasks_layout.count()):
            widget = self.subtasks_layout.itemAt(i).widget()
            if widget:
                label = widget.findChild(QLabel)
                if label:
                    subtasks.append(label.text())
        dialog.subtasks_input.setText("; ".join(subtasks))
        
        if dialog.exec() == QDialog.Accepted:
            # Обновляем данные в карточке
            self.task_name.setText(dialog.get_task_name())
            self.task_description.setText(dialog.get_description())
            self.top_info.setText(f"{self.format_date(dialog.get_due_date())} • {self.get_priority_text(dialog.get_priority())}")
            
            # Обновляем подзадачи
            for i in reversed(range(self.subtasks_layout.count())):
                self.subtasks_layout.itemAt(i).widget().deleteLater()
            
            subtasks = dialog.get_subtasks()
            if subtasks:
                subtasks_list = [subtask.strip() for subtask in subtasks.split(';') if subtask.strip()]
                for i, subtask in enumerate(subtasks_list, 1):
                    subtask_widget = QWidget()
                    subtask_widget.setFixedHeight(32)  # Увеличиваем высоту контейнера
                    subtask_layout = QHBoxLayout(subtask_widget)
                    subtask_layout.setContentsMargins(0, 0, 0, 0)
                    subtask_layout.setSpacing(8)
                    
                    subtask = SubtaskWidget(subtask)
                    subtask.checkbox.clicked.connect(lambda checked, w=subtask: self.handle_subtask_click(checked, w))
                    subtask_layout.addWidget(subtask)
                    
                    self.subtasks_layout.addWidget(subtask_widget)
                
                self.subtasks_label.setVisible(True)
                self.subtasks_scroll.setVisible(True)
            else:
                self.subtasks_label.setVisible(False)
                self.subtasks_scroll.setVisible(False)
            
            # Обновляем данные в JSON
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Находим задачу по ID
                task_list = data[0]
                for task in task_list['tasks']:
                    if task['id'] == self.task_id:
                        task['task_name'] = dialog.get_task_name()
                        task['task_description'] = dialog.get_description()
                        task['task_priority'] = dialog.get_priority()
                        task['task_due_date'] = dialog.get_due_date()
                        
                        # Обновляем подзадачи
                        task['task_subtasks'] = []
                        if subtasks:
                            subtasks_list = [subtask.strip() for subtask in subtasks.split(';') if subtask.strip()]
                            for i, subtask in enumerate(subtasks_list, 1):
                                task['task_subtasks'].append({
                                    "id": i,
                                    "subtask_name": subtask
                                })
                        break
                
                # Сохраняем обновленные данные
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    
            except Exception as e:
                print(f"Ошибка при обновлении задачи: {e}")

    def handle_task_click(self, checked):
        # Зачеркиваем или возвращаем текст названия задачи
        if checked:
            self.task_name.setStyleSheet("text-decoration: line-through; color: #666666;")
            # Перемещаем виджет в конец списка
            self.parent.tasks_layout.removeWidget(self)
            self.parent.tasks_layout.addWidget(self)
            
            # Перемещаем задачу в конец списка всех задач
            if hasattr(self.parent, 'all_tasks_layout'):
                self.parent.all_tasks_layout.removeWidget(self)
                self.parent.all_tasks_layout.addWidget(self)
            
            # Отмечаем все подзадачи как выполненные
            for i in range(self.subtasks_layout.count()):
                widget = self.subtasks_layout.itemAt(i).widget()
                if widget:
                    checkbox = widget.findChild(QCheckBox)
                    label = widget.findChild(QLabel)
                    if checkbox and label:
                        checkbox.setChecked(True)
                        label.setStyleSheet("text-decoration: line-through; color: #666666;")
        else:
            self.task_name.setStyleSheet("")
            # Перемещаем виджет в начало списка
            self.parent.tasks_layout.removeWidget(self)
            self.parent.tasks_layout.insertWidget(0, self)
            
            # Перемещаем задачу в начало списка всех задач
            if hasattr(self.parent, 'all_tasks_layout'):
                self.parent.all_tasks_layout.removeWidget(self)
                self.parent.all_tasks_layout.insertWidget(0, self)
            
            # Снимаем отметки со всех подзадач
            for i in range(self.subtasks_layout.count()):
                widget = self.subtasks_layout.itemAt(i).widget()
                if widget:
                    checkbox = widget.findChild(QCheckBox)
                    label = widget.findChild(QLabel)
                    if checkbox and label:
                        checkbox.setChecked(False)
                        label.setStyleSheet("")
        
        # Обновляем состояние в JSON
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Находим задачу по ID
            task_list = data[0]
            for task in task_list['tasks']:
                if task['id'] == self.task_id:
                    task['task_is_done'] = checked
                    # Обновляем состояние подзадач
                    for subtask in task['task_subtasks']:
                        subtask['is_completed'] = checked
                    break
            
            # Сохраняем обновленные данные
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"Ошибка при сохранении состояния задачи: {e}")

    def handle_subtask_click(self, checked, widget):
        # Обновляем стиль подзадачи
        widget.update_style()
        
        # Сохраняем состояние в JSON
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Находим задачу по ID
            task_list = data[0]
            for task in task_list['tasks']:
                if task['id'] == self.task_id:
                    # Находим подзадачу по тексту
                    label = widget.label
                    if label:
                        subtask_text = label.text()
                        # Находим и обновляем подзадачу
                        for subtask in task['task_subtasks']:
                            if subtask['subtask_name'] == subtask_text:
                                subtask['is_completed'] = checked
                                if checked:
                                    # Перемещаем подзадачу в конец списка
                                    task['task_subtasks'].remove(subtask)
                                    task['task_subtasks'].append(subtask)
                                else:
                                    # Перемещаем подзадачу в начало списка
                                    task['task_subtasks'].remove(subtask)
                                    task['task_subtasks'].insert(0, subtask)
                                break
                    break
            
            # Сохраняем обновленные данные
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"Ошибка при сохранении состояния подзадачи: {e}")

class SubtaskWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        
        # Основной layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Чекбокс
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(20, 20)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 0px;
                margin: 0px;
                padding: 0px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 1px solid #353028;
                border-radius: 4px;
                margin: 0px;
                padding: 0px;
            }
            QCheckBox::indicator:checked {
                background-color: #6C946D;
                border: none;
                image: url(check.png);
            }
            QCheckBox::indicator:hover {
                border-color: #8AB38B;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #8AB38B;
            }
        """)
        layout.addWidget(self.checkbox, 0, Qt.AlignVCenter)
        
        # Текст подзадачи
        self.label = QLabel(text)
        self.label.setFixedHeight(32)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #353028;
                font-weight: 300;
                padding: 0px;
                margin: 0px;
                line-height: 32px;
            }
        """)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addWidget(self.label, 1)
        
        # Устанавливаем курсор на весь виджет
        self.setCursor(Qt.PointingHandCursor)
        
    def mousePressEvent(self, event):
        self.checkbox.setChecked(not self.checkbox.isChecked())
        self.update_style()
        super().mousePressEvent(event)
        
    def update_style(self):
        if self.checkbox.isChecked():
            self.label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #666666;
                    font-weight: 300;
                    padding: 0px;
                    margin: 0px;
                    line-height: 32px;
                    text-decoration: line-through;
                }
            """)
        else:
            self.label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #353028;
                    font-weight: 300;
                    padding: 0px;
                    margin: 0px;
                    line-height: 32px;
                }
            """)