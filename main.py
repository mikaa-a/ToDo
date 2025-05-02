import sys
import json
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame
from PySide6.QtCore import QFile, Qt, QDate
from ui_mainwindow import Ui_Form
from dialog import AddTaskDialog

class TaskCard(QWidget):
    def __init__(self, text: str, date: str, priority: str, description: str, sub_tasks: str):
        super().__init__()
        
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

        if not sub_tasks:
            self.subtasks_label.setVisible(False)
        else:
            self.subtasks_label.setVisible(True)
        
        self.task_sub_tasks = QLabel(sub_tasks)
        self.task_sub_tasks.setObjectName("task_sub_tasks")
        self.main_layout.addWidget(self.task_sub_tasks)

        # Кнопка редактирования
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setFixedWidth(100)
        self.main_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)

        # Устанавливаем layout для основного виджета
        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)

    def get_priority_text(self, priority: int):
        match priority:
            case 1:
                return "Низкий"
            case 2:
                return "Средний"
            case 3:
                return "Высокий"
            case 0:
                return "Не задан"
            case _:
                return "Не задан"

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
  
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.tasks_layout.setSpacing(10)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)

        self.ui.tasks_scroll_area.setWidget(self.tasks_widget)
        self.ui.tasks_scroll_area.setWidgetResizable(True)
        self.ui.tasks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tasks_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.add_task_btn.clicked.connect(self.show_add_task_dialog)
        
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
                            subtasks_text = "\n".join([subtask['subtask_name'] for subtask in task['task_subtasks']])
                        
                        # Добавляем задачу в интерфейс
                        self.add_task_to_layout(
                            task['task_name'],
                            task['task_due_date'],
                            task['task_priority'],
                            task['task_description'],
                            subtasks_text
                        )
        except Exception as e:
            print(f"Ошибка при загрузке задач: {e}")

    def add_task_to_layout(self, text: str, date: str, priority: str, description: str, sub_tasks: str):
        task = TaskCard(text, date, priority, description, sub_tasks)
        self.tasks_layout.addWidget(task)

    def show_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.Accepted:
            task_name = dialog.get_task_name()
            date = dialog.get_due_date()
            priority = dialog.get_priority()
            description = dialog.get_description()
            sub_tasks = dialog.get_subtasks()
           
            if not task_name:
                return
            
            self.add_task_to_layout(task_name, date, priority, description, sub_tasks)


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