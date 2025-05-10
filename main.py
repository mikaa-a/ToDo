import sys
import json
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame, QMessageBox
from PySide6.QtCore import QFile, Qt, QDate
from ui_mainwindow import Ui_Form
from dialog import AddTaskDialog, EditListDialog

class TaskCard(QWidget):
    def __init__(self, text: str, date: str, priority: str, description: str, sub_tasks: str, task_id: int, parent=None):
        super().__init__()
        self.task_id = task_id
        self.parent = parent
        
        # Создаем контейнер для стилей
        self.container = QFrame()
        self.container.setObjectName("task_card")
        self.container.setStyleSheet("""
            QFrame#task_card {
                background-color: #B1CCBB;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        
        # Основной layout для контейнера
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Верхняя часть с названием, датой и приоритетом
        self.top_layout = QHBoxLayout()
        
        # Чекбокс и название задачи
        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("task_checkbox")
        self.checkbox.clicked.connect(self.handle_task_click)  # Подключаем обработчик
        self.top_layout.addWidget(self.checkbox)
        
        self.task_name = QLabel(text)
        self.task_name.setObjectName("task_name")
        self.top_layout.addSpacing(8)
        self.top_layout.addWidget(self.task_name)
        
        # Добавляем растягивающийся элемент
        self.top_layout.addStretch()
        
        # Дата и приоритет
        self.top_info = QLabel(f"{self.format_date(date)} • {self.get_priority_text(priority)}")
        self.top_info.setObjectName("task_top_info")
        self.top_layout.addWidget(self.top_info)
        
        self.main_layout.addLayout(self.top_layout)

        # Описание
        self.description_label = QLabel("Описание:")
        self.description_label.setObjectName("description_label")
        self.main_layout.addWidget(self.description_label)

        if not description:
            self.description_label.setVisible(False)
        else:
            self.description_label.setVisible(True)

        self.task_description = QLabel(description)
        self.task_description.setObjectName("task_description")
        self.main_layout.addWidget(self.task_description)

        # Подзадачи
        self.subtasks_label = QLabel("Подзадачи:")
        self.subtasks_label.setObjectName("subtasks_label")
        self.main_layout.addWidget(self.subtasks_label)

        # Создаем контейнер для подзадач с прокруткой
        self.subtasks_scroll = QScrollArea()
        self.subtasks_scroll.setWidgetResizable(True)
        self.subtasks_scroll.setMaximumHeight(150)  # Максимальная высота
        self.subtasks_scroll.setMinimumHeight(0)    # Минимальная высота
        self.subtasks_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.subtasks_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
            total_height = len(subtasks_list) * 30  # Примерная высота одной подзадачи
            if total_height < 150:
                self.subtasks_scroll.setFixedHeight(total_height + 20)  # Добавляем отступы
            else:
                self.subtasks_scroll.setFixedHeight(150)
                
            for i, subtask in enumerate(subtasks_list, 1):
                subtask_widget = QWidget()
                subtask_layout = QHBoxLayout(subtask_widget)
                subtask_layout.setContentsMargins(0, 0, 0, 0)
                subtask_layout.setSpacing(4)
                
                checkbox = QCheckBox()
                checkbox.setObjectName("task_checkbox")
                checkbox.setStyleSheet("""
                    QCheckBox {
                        spacing: 5px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                        border: 1px solid #353028;
                        border-radius: 3px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #6C946D;
                        border: none;
                    }
                    QCheckBox::indicator:hover {
                        border-color: #8AB38B;
                    }
                    QCheckBox::indicator:checked:hover {
                        background-color: #8AB38B;
                    }
                """)
                checkbox.clicked.connect(lambda checked, w=subtask_widget: self.handle_subtask_click(checked, w))
                subtask_layout.addWidget(checkbox)
                
                label = QLabel(subtask)
                label.setObjectName(f"subtask_label_{i}")
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setCursor(Qt.PointingHandCursor)
                label.mousePressEvent = lambda event, cb=checkbox, w=subtask_widget: self.toggle_subtask_checkbox(event, cb, w)
                subtask_layout.addWidget(label)
                
                subtask_layout.addStretch()
                
                self.subtasks_layout.addWidget(subtask_widget)
        else:
            self.subtasks_label.setVisible(False)
            self.subtasks_scroll.setVisible(False)

        # Кнопка редактирования
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setFixedWidth(100)
        self.edit_button.clicked.connect(self.edit_task)
        self.main_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)

        # Устанавливаем layout для основного виджета
        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)

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
                    subtask_layout = QHBoxLayout(subtask_widget)
                    subtask_layout.setContentsMargins(0, 0, 0, 0)
                    subtask_layout.setSpacing(4)
                    
                    checkbox = QCheckBox()
                    checkbox.setObjectName(f"subtask_checkbox_{i}")
                    subtask_layout.addWidget(checkbox)
                    
                    label = QLabel(subtask)
                    label.setObjectName(f"subtask_label_{i}")
                    label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    label.setCursor(Qt.PointingHandCursor)
                    label.mousePressEvent = lambda event, cb=checkbox, w=subtask_widget: self.toggle_subtask_checkbox(event, cb, w)
                    subtask_layout.addWidget(label)
                    
                    subtask_layout.addStretch()
                    
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
        # Зачеркиваем или возвращаем текст
        label = widget.findChild(QLabel)
        if label:
            if checked:
                label.setStyleSheet("text-decoration: line-through; color: #666666;")
                # Перемещаем виджет в конец списка
                self.subtasks_layout.removeWidget(widget)
                self.subtasks_layout.addWidget(widget)
            else:
                label.setStyleSheet("")
                # Перемещаем виджет в начало списка
                self.subtasks_layout.removeWidget(widget)
                self.subtasks_layout.insertWidget(0, widget)
                
        # Сохраняем состояние в JSON
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Находим задачу по ID
            task_list = data[0]
            for task in task_list['tasks']:
                if task['id'] == self.task_id:
                    # Находим подзадачу по тексту
                    label = widget.findChild(QLabel)
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

    def toggle_subtask_checkbox(self, event, checkbox, widget):
        # Переключаем состояние чекбокса
        checkbox.setChecked(not checkbox.isChecked())
        # Вызываем обработчик изменения состояния
        self.handle_subtask_click(checkbox.isChecked(), widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.ui = Ui_Form()
        self.ui.setupUi(self.central_widget)

        self.MARGIN = 20
        self.ui.content.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)

        self.tasks_widget = QWidget()
        self.tasks_widget.setObjectName("tasks_widget")
  
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.tasks_layout.setSpacing(10)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)

        self.ui.tasks_scroll_area.setWidget(self.tasks_widget)
        self.ui.tasks_scroll_area.setWidgetResizable(True)
        self.ui.tasks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tasks_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Инициализация комбо бокса для сортировки
        self.ui.sort_layout.setAlignment(Qt.AlignLeft)
        self.ui.priority_sort_select.addItems(["По возрастанию", "По убыванию", "Все приоритеты"])
        self.ui.sort_btn.setText("Применить")
        self.ui.sort_btn.clicked.connect(self.sort_tasks)
    
        self.ui.add_task_btn.clicked.connect(self.show_add_task_dialog)
        self.ui.edit_list_btn.clicked.connect(self.show_edit_list_dialog)
        
        # Загружаем задачи при инициализации
        self.load_tasks_from_json()

        self.ui.content.setCurrentIndex(1)  # Show list_page at startup for testing

    def load_tasks_from_json(self):
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                if data and len(data) > 0:
                    # Берем первый список задач
                    first_list = data[0]
                    for task in first_list['tasks']:
                        # Форматируем подзадачи в строку
                        subtasks_text = ""
                        if task['task_subtasks']:
                            subtasks_text = "; ".join([subtask['subtask_name'] for subtask in task['task_subtasks']])
                        
                        # Добавляем задачу в интерфейс
                        self.add_task_to_layout(
                            task['task_name'],
                            task['task_due_date'],
                            task['task_priority'],
                            task['task_description'],
                            subtasks_text,
                            task['id']
                        )
        except Exception as e:
            print(f"Ошибка при загрузке задач: {e}")

    def add_task_to_layout(self, text: str, date: str, priority: str, description: str, sub_tasks: str, task_id: int):
        task = TaskCard(text, date, priority, description, sub_tasks, task_id, self)
        self.tasks_layout.addWidget(task)

    def show_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.Accepted:
            task_name = dialog.get_task_name()
            date = dialog.get_due_date()
            priority = dialog.get_priority()
            description = dialog.get_description()
            sub_tasks = dialog.get_subtasks()
            
            # Добавляем задачу в интерфейс
            self.add_task_to_layout(task_name, date, priority, description, sub_tasks, self.tasks_layout.count() + 1)
            
            # Сохраняем задачу в JSON
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Получаем первый список задач
                task_list = data[0]
                
                # Создаем новую задачу
                new_task = {
                    "id": len(task_list['tasks']) + 1,
                    "task_name": task_name,
                    "task_description": description,
                    "task_priority": priority,
                    "task_due_date": date,
                    "task_is_done": False,
                    "task_subtasks": []
                }
                
                # Добавляем подзадачи
                if sub_tasks:
                    subtasks_list = [subtask.strip() for subtask in sub_tasks.split(';') if subtask.strip()]
                    for i, subtask in enumerate(subtasks_list, 1):
                        new_task["task_subtasks"].append({
                            "id": i,
                            "subtask_name": subtask,
                            "is_completed": False
                        })
                
                # Добавляем задачу в список
                task_list['tasks'].append(new_task)
                
                # Сохраняем обновленные данные
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    
            except Exception as e:
                print(f"Ошибка при сохранении задачи: {e}")

    def show_edit_list_dialog(self):
        dialog = EditListDialog(self.ui.list_text.text(), self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Обновляем название списка
            new_name = dialog.get_list_name()
            if new_name.strip():
                self.ui.list_text.setText(new_name)
                # Обновляем название в JSON
                try:
                    with open('data.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    data[0]['list_name'] = new_name
                    with open('data.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"Ошибка при обновлении названия списка: {e}")
        elif result == 2:  # Код удаления списка
            # Удаляем все задачи из интерфейса
            while self.tasks_layout.count():
                item = self.tasks_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Очищаем JSON файл
            try:
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump([{
                        "list_name": "Новый список",
                        "id": 1,
                        "tasks": []
                    }], file, ensure_ascii=False, indent=4)
                self.ui.list_text.setText("Новый список")
            except Exception as e:
                print(f"Ошибка при удалении списка: {e}")

    def sort_tasks(self):
        # Получаем текущий выбор из комбо бокса
        sort_type = self.ui.priority_sort_select.currentText()
        
        # Получаем все задачи из layout
        tasks = []
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            if item.widget():
                tasks.append(item.widget())
        
        # Сортируем задачи в зависимости от выбранного типа
        if sort_type == "по возрастанию":
            tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()))
        elif sort_type == "по убыванию":
            tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()), reverse=True)
        
        # Добавляем отсортированные задачи обратно в layout
        for task in tasks:
            self.tasks_layout.addWidget(task)

    def get_priority_value(self, priority_text):
        priority_map = {
            "Низкий приоритет": 1,
            "Средний приоритет": 2,
            "Высокий приоритет": 3,
            "Приоритет не задан": 0
        }
        return priority_map.get(priority_text, 0)

def load_stylesheet(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            styles = f.read()
            return styles
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