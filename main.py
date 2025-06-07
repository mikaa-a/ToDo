import sys
import json
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame, QMessageBox, QLayout, QComboBox
from PySide6.QtCore import QFile, Qt, QDate, QRect
from ui_mainwindow import Ui_Form
from dialogs.dialog import AddTaskDialog, EditListDialog
from tasks.task_card import TaskCard
from utils.helpers import load_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setMinimumSize(1000, 600)

        # Создаем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем главный лейаут для центрального виджета
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)  # Убираем нижний отступ
        self.central_layout.setSpacing(0)

        # Создаем контейнер для основного контента
        content_container = QWidget()
        content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Инициализируем UI
        self.ui = Ui_Form()
        self.ui.setupUi(content_container)
        self.stacked_widget = self.ui.content

        # Удаляем старую геометрию content
        self.ui.content.setGeometry(QRect())
        self.ui.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Добавляем content в контейнер контента
        content_layout.addWidget(self.ui.content)

        # Добавляем контейнер контента в центральный лейаут
        self.central_layout.addWidget(content_container)

        # Настраиваем страницу списка
        self.ui.list_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Создаем главный лейаут для страницы списка
        self.list_page_layout = QVBoxLayout(self.ui.list_page)
        self.list_page_layout.setContentsMargins(38, 38, 38, 38)
        self.list_page_layout.setSpacing(10)  # Уменьшаем расстояние между элементами с 20 до 10 пикселей

        # Создаем верхний лейаут для заголовка и кнопок
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(10)
        self.header_layout.setAlignment(Qt.AlignLeft)  # Устанавливаем выравнивание всего лейаута по левому краю
        
        # Настраиваем размеры заголовка списка
        self.ui.list_text.setMinimumHeight(40)
        self.ui.list_text.setMinimumWidth(200)
        self.ui.list_text.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.list_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.ui.list_text.setContentsMargins(0, 0, 0, 0)
        self.ui.list_text.setStyleSheet("margin: 0; padding: 0;")  # Убираем все возможные отступы через стили
        
        # Создаем контейнер для заголовка
        header_container = QWidget()
        header_container.setContentsMargins(0, 0, 0, 0)
        header_container_layout = QHBoxLayout(header_container)
        header_container_layout.setContentsMargins(0, 0, 0, 0)
        header_container_layout.setSpacing(0)
        header_container_layout.addWidget(self.ui.list_text)
        
        # Добавляем элементы в header_layout
        self.header_layout.addWidget(header_container)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.ui.add_task_btn)
        self.header_layout.addWidget(self.ui.edit_list_btn)
        
        # Устанавливаем выравнивание по вертикали для кнопок
        self.ui.add_task_btn.setFixedHeight(self.ui.list_text.height())
        self.ui.edit_list_btn.setFixedHeight(self.ui.list_text.height())
        
        # Добавляем header_layout в главный лейаут
        self.list_page_layout.addLayout(self.header_layout)

        # Добавляем кнопку "Вернуться к спискам"
        self.list_page_layout.addWidget(self.ui.back_to_list_btn)

        # Создаем лейаут для сортировки
        self.sort_layout = QHBoxLayout()
        self.sort_layout.setContentsMargins(0, 0, 0, 0)
        self.sort_layout.setSpacing(8)
        
        # Добавляем элементы сортировки
        self.sort_layout.addWidget(self.ui.priority_sort_select)
        self.sort_layout.addWidget(self.ui.sort_btn)
        self.sort_layout.addStretch()
        
        # Добавляем лейаут сортировки в главный лейаут
        self.list_page_layout.addLayout(self.sort_layout)

        # Создаем контейнер для области прокрутки
        scroll_container = QWidget()
        scroll_container.setObjectName("scroll_container")
        scroll_container_layout = QHBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(0, 0, 0, 0)
        scroll_container_layout.setSpacing(0)
        
        # Настраиваем область прокрутки
        self.ui.tasks_scroll_area.setWidgetResizable(True)
        self.ui.tasks_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.tasks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tasks_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Делаем адаптивную ширину
        self.ui.tasks_scroll_area.setMinimumWidth(600)  # Минимальная ширина
        self.ui.tasks_scroll_area.setMinimumHeight(0)
        
        # Создаем виджет для задач
        self.tasks_widget = QWidget()
        self.tasks_widget.setObjectName("tasks_widget")
        self.tasks_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Создаем лейаут для задач
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.tasks_layout.setSpacing(10)
        self.tasks_layout.setContentsMargins(0, 0, 0, 72)  # Увеличиваем нижний отступ до 72px (51px меню + 21px дополнительный отступ)
        
        # Устанавливаем виджет задач в область прокрутки
        self.ui.tasks_scroll_area.setWidget(self.tasks_widget)
        
        # Добавляем область прокрутки в главный лейаут
        self.list_page_layout.addWidget(self.ui.tasks_scroll_area)

        # Создаем контейнер для нижнего меню
        bottom_menu_container = QWidget()
        bottom_menu_container.setObjectName("bottom_menu_container")
        bottom_menu_layout = QHBoxLayout(bottom_menu_container)
        bottom_menu_layout.setContentsMargins(0, 0, 0, 0)
        bottom_menu_layout.setSpacing(0)
        bottom_menu_layout.setAlignment(Qt.AlignHCenter)
        
        # Настраиваем внутренний лейаут меню
        self.ui.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.top_bar_layout.setSpacing(5)  # Минимальное расстояние между кнопками
        self.ui.top_bar_layout.setAlignment(Qt.AlignCenter)
        
        # Настраиваем кнопки меню
        for button in [self.ui.all_task_btn, self.ui.all_lists_btn, self.ui.focus_mode_btn]:
            button.setFixedSize(50, 50)
            button.setContentsMargins(0, 0, 0, 0)
            button.setStyleSheet("margin: 0; padding: 0;")
        
        bottom_menu_layout.addWidget(self.ui.horizontalLayoutWidget_2)

        # Добавляем контейнер с меню в центральный лейаут
        self.central_layout.addWidget(bottom_menu_container)

        # Удаляем старые виджеты
        old_widgets = []
        for attr_name in ['tasks_container', 'verticalLayoutWidget', 'layoutWidget1', 'horizontalLayoutWidget']:
            if hasattr(self.ui, attr_name):
                widget = getattr(self.ui, attr_name)
                if widget:
                    old_widgets.append(widget)
                    setattr(self.ui, attr_name, None)  # Очищаем ссылку в UI

        # Удаляем виджеты после очистки ссылок
        for widget in old_widgets:
            try:
                if widget.parent():
                    widget.setParent(None)
                widget.deleteLater()
            except RuntimeError:
                pass  # Игнорируем ошибки с уже удаленными виджетами

        # Устанавливаем текущую страницу
        self.stacked_widget.setCurrentIndex(1)  # Show list_page at startup

        # Инициализация комбо бокса для сортировки
        self.ui.sort_layout.setAlignment(Qt.AlignLeft)
        self.ui.priority_sort_select.addItems(["По возрастанию", "По убыванию", "Все приоритеты"])
        self.ui.sort_btn.setText("Применить")
        self.ui.sort_btn.clicked.connect(self.sort_tasks)
    
        self.ui.add_task_btn.clicked.connect(self.show_add_task_dialog)
        self.ui.edit_list_btn.clicked.connect(self.show_edit_list_dialog)
        
        # Загружаем задачи при инициализации
        self.load_tasks_from_json()

        # Устанавливаем текст для кнопок нижнего меню
        self.ui.all_task_btn.setText("1")
        self.ui.all_lists_btn.setText("2")
        self.ui.focus_mode_btn.setText("3")

        # Подключаем обработчики для кнопок нижнего меню
        self.ui.focus_mode_btn.clicked.connect(self.show_focus_page)
        self.ui.all_task_btn.clicked.connect(self.show_all_tasks_page)
        self.ui.all_lists_btn.clicked.connect(self.show_all_lists_page)

        # Подключаем обработчик изменения размера окна
        self.resizeEvent = self.handle_resize

    def handle_resize(self, event):
        # Обновляем размеры при изменении размера окна
        super().resizeEvent(event)
        self.ui.content.setMinimumSize(self.width(), self.height())
        self.ui.list_page.setMinimumSize(self.ui.content.size())

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
        if sort_type == "По возрастанию":
            tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()))
        elif sort_type == "По убыванию":
            tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()), reverse=True)
        elif sort_type == "Все приоритеты":
            tasks.sort(key=lambda x: self.get_date_value(x.top_info.text().split(' • ')[0].strip()))
        
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

    def get_date_value(self, date_text):
        try:
            # Преобразуем строку даты в объект QDate
            day, month, year = map(int, date_text.split('.'))
            task_date = QDate(year, month, day)
            current_date = QDate.currentDate()
            
            # Возвращаем количество дней между текущей датой и датой задачи
            # Используем abs() чтобы получить абсолютное значение разницы
            return abs(current_date.daysTo(task_date))
        except:
            # В случае ошибки парсинга даты возвращаем максимальное значение
            return float('inf')

    def show_all_tasks_page(self):
        self.stacked_widget.setCurrentIndex(4)  # Переключаем на focus_page

    def show_all_lists_page(self):
        self.stacked_widget.setCurrentIndex(3)  # Переключаем на focus_page

    def show_focus_page(self):
        self.stacked_widget.setCurrentIndex(2)  # Переключаем на focus_page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet = load_stylesheet('styles.qss')

    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())