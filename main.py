import sys
import json
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame, QMessageBox, QLayout, QComboBox
from PySide6.QtCore import QFile, Qt, QDate, QRect
from ui_mainwindow import Ui_Form
from dialogs.dialog import AddTaskDialog, EditListDialog
from tasks.task_card import TaskCard
from utils.helpers import load_stylesheet

class ListCard(QWidget):
    def __init__(self, list_name, uncompleted_task_count, list_index, main_window_instance, parent=None):
        super().__init__(parent)
        self.list_index = list_index
        self.main_window_instance = main_window_instance
        self.init_ui(list_name, uncompleted_task_count)
        
        # Устанавливаем политику размеров для карточки
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumWidth(0)  # Позволяем карточке сжиматься

    def init_ui(self, list_name, uncompleted_task_count):
        # Создаем контейнер для стилей
        self.container = QFrame()
        self.container.setObjectName("list_card_frame")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.container.setMinimumWidth(0)  # Позволяем контейнеру сжиматься
        
        # Основной layout для контейнера
        self.main_layout = QHBoxLayout(self.container)
        self.main_layout.setContentsMargins(20, 15, 20, 15)
        self.main_layout.setSpacing(20)
        
        # Создаем вертикальный layout для текста (перемещаем его выше)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        # Добавляем название списка
        name_label = QLabel(list_name)
        name_label.setObjectName("list_name")
        text_layout.addWidget(name_label)
        
        # Добавляем количество невыполненных задач
        count_text = f"{uncompleted_task_count} {'невыполненная задача' if uncompleted_task_count == 1 else 'невыполненных задачи' if 1 < uncompleted_task_count < 5 else 'невыполненных задач'}"
        count_label = QLabel(count_text)
        count_label.setObjectName("list_task_count")
        text_layout.addWidget(count_label)
        
        self.main_layout.addLayout(text_layout) # Добавляем текстовый layout в основной
        self.main_layout.addStretch()
        
        # Устанавливаем курсор в виде руки при наведении
        self.setCursor(Qt.PointingHandCursor)

        # Устанавливаем layout для основного виджета
        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Вызываем метод open_list у экземпляра MainWindow
            self.main_window_instance.open_list(self)

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
        
        # Настраиваем страницу "Мои списки" для расширения
        self.ui.my_lists.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.lists_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tasks_container_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
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
        self.ui.tasks_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tasks_scroll_area.setMinimumWidth(600)
        self.ui.tasks_scroll_area.setMinimumHeight(0)
        self.ui.tasks_scroll_area.setStyleSheet("QScrollArea { background-color: #F3F2F3; }")
        
        # Создаем виджет для задач
        self.tasks_widget = QWidget()
        self.tasks_widget.setObjectName("tasks_widget")
        self.tasks_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tasks_widget.setStyleSheet("background-color: #F3F2F3;")
        
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

        # Инициализация комбо боксов для сортировки
        self.ui.sort_layout.setAlignment(Qt.AlignLeft)
        self.ui.sort_layout_2.setAlignment(Qt.AlignLeft)
        
        # Выравнивание для списка карточек на странице "Мои списки"
        self.ui.tasks_layout_3.setAlignment(Qt.AlignTop)
        
        # Настройка комбо бокса для списка
        self.ui.priority_sort_select.addItems(["По возрастанию", "По убыванию", "Все приоритеты"])
        self.ui.sort_btn.setText("Применить")
        self.ui.sort_btn.clicked.connect(self.sort_tasks)
        
        # Настройка комбо бокса для всех задач
        self.ui.priority_sort_select_2.addItems(["По возрастанию", "По убыванию", "Все приоритеты"])
        self.ui.sort_btn_2.setText("Применить")
        self.ui.sort_btn_2.clicked.connect(self.sort_all_tasks)

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

        # Подключаем обработчик для кнопки добавления задачи в окне "Все задачи"
        self.ui.add_task_2.clicked.connect(self.show_add_task_from_all_tasks)

        # Подключаем обработчик изменения размера окна
        self.resizeEvent = self.handle_resize

        # Настраиваем корневой макет для страницы "Мои списки"
        self.my_lists_layout = QVBoxLayout(self.ui.my_lists)
        self.my_lists_layout.setContentsMargins(38, 38, 38, 38)
        self.my_lists_layout.setSpacing(10)
        self.my_lists_layout.addWidget(self.ui.horizontalLayoutWidget_3)
        self.my_lists_layout.addWidget(self.ui.lists_scroll_area)

        # Создаем лейаут для всех задач
        self.all_tasks_layout = QVBoxLayout(self.ui.tasks_container_4)
        self.all_tasks_layout.setAlignment(Qt.AlignTop)
        self.all_tasks_layout.setSpacing(10)
        self.all_tasks_layout.setContentsMargins(0, 0, 0, 72)  # Возвращаем стандартные отступы

        # Настраиваем область прокрутки для всех задач
        self.ui.all_tasks_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.all_tasks_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.all_tasks_scroll_area.setWidgetResizable(True)
        self.ui.all_tasks_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.all_tasks_scroll_area.setMinimumWidth(600)
        self.ui.all_tasks_scroll_area.setMinimumHeight(0)
        self.ui.all_tasks_scroll_area.setStyleSheet("QScrollArea { background-color: #F3F2F3; }")
        
        # Создаем виджет для всех задач
        self.all_tasks_widget = QWidget()
        self.all_tasks_widget.setObjectName("all_tasks_widget")
        self.all_tasks_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.all_tasks_widget.setStyleSheet("background-color: #F3F2F3;")
        
        # Создаем лейаут для всех задач
        self.all_tasks_layout = QVBoxLayout(self.all_tasks_widget)
        self.all_tasks_layout.setAlignment(Qt.AlignTop)
        self.all_tasks_layout.setSpacing(10)
        self.all_tasks_layout.setContentsMargins(0, 0, 0, 72)
        
        # Устанавливаем виджет задач в область прокрутки
        self.ui.all_tasks_scroll_area.setWidget(self.all_tasks_widget)

        # Создаем новый контейнер для страницы "Все задачи"
        self.all_tasks_container = QWidget()
        self.all_tasks_container.setObjectName("all_tasks_container")
        self.all_tasks_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Создаем корневой макет для страницы "Все задачи"
        self.all_tasks_page_layout = QVBoxLayout(self.all_tasks_container)
        self.all_tasks_page_layout.setContentsMargins(38, 38, 38, 38)
        self.all_tasks_page_layout.setSpacing(10)
        
        # Создаем верхний лейаут для заголовка и кнопок
        self.all_tasks_header_layout = QHBoxLayout()
        self.all_tasks_header_layout.setContentsMargins(0, 0, 0, 0)
        self.all_tasks_header_layout.setSpacing(10)
        self.all_tasks_header_layout.setAlignment(Qt.AlignVCenter)  # Выравнивание по вертикали по центру
        
        # Создаем заголовок для страницы "Все задачи"
        self.all_tasks_label = QLabel("Все задачи")
        self.all_tasks_label.setObjectName("all_tasks_label")
        self.all_tasks_label.setMinimumHeight(42)
        self.all_tasks_label.setMinimumWidth(509)
        self.all_tasks_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.all_tasks_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        # Настраиваем кнопку добавления задачи
        self.ui.add_task_2.setFixedHeight(42)  # Устанавливаем такую же высоту как у заголовка
        self.ui.add_task_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Добавляем элементы в header_layout
        self.all_tasks_header_layout.addWidget(self.all_tasks_label)
        self.all_tasks_header_layout.addStretch()
        self.all_tasks_header_layout.addWidget(self.ui.add_task_2)
        
        # Добавляем header_layout в корневой макет
        self.all_tasks_page_layout.addLayout(self.all_tasks_header_layout)
        
        # Создаем лейаут для сортировки
        self.all_tasks_sort_layout = QHBoxLayout()
        self.all_tasks_sort_layout.setContentsMargins(0, 0, 0, 0)
        self.all_tasks_sort_layout.setSpacing(8)
        
        # Добавляем элементы сортировки
        self.all_tasks_sort_layout.addWidget(self.ui.priority_sort_select_2)
        self.all_tasks_sort_layout.addWidget(self.ui.sort_btn_2)
        self.all_tasks_sort_layout.addStretch()
        
        # Добавляем лейаут сортировки в корневой макет
        self.all_tasks_page_layout.addLayout(self.all_tasks_sort_layout)
        
        # Добавляем область прокрутки в корневой макет
        self.all_tasks_page_layout.addWidget(self.ui.all_tasks_scroll_area)

        # Заменяем старый контейнер на новый в stacked widget
        # Используем фиксированный индекс 3 для страницы "Все задачи"
        ALL_TASKS_PAGE_INDEX = 3
        
        # Удаляем старый контейнер, если он существует
        try:
            old_widget = self.ui.content.widget(ALL_TASKS_PAGE_INDEX)
            if old_widget:
                self.ui.content.removeWidget(old_widget)
                old_widget.deleteLater()
        except:
            pass  # Игнорируем ошибки при удалении старого виджета
        
        # Добавляем новый контейнер
        self.ui.content.insertWidget(ALL_TASKS_PAGE_INDEX, self.all_tasks_container)
        
        # Очищаем ссылку на старый контейнер
        self.ui.tasks_container_4 = None

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
        self.stacked_widget.setCurrentIndex(3)  # Переключаем на страницу всех задач
        self.load_all_tasks()  # Загружаем все задачи

    def show_all_lists_page(self):
        self.stacked_widget.setCurrentIndex(4)  # Переключаем на страницу списков
        self.load_lists()  # Загружаем списки

    def show_focus_page(self):
        self.stacked_widget.setCurrentIndex(2)  # Переключаем на focus_page

    def sort_all_tasks(self):
        # Получаем текущий выбор из комбо бокса
        sort_type = self.ui.priority_sort_select_2.currentText()
        
        # Получаем все задачи из layout
        tasks = []
        while self.all_tasks_layout.count():
            item = self.all_tasks_layout.takeAt(0)
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
            self.all_tasks_layout.addWidget(task)

    def show_add_task_from_all_tasks(self):
        dialog = AddTaskDialog(self, from_all_tasks=True)
        if dialog.exec() == QDialog.Accepted:
            task_name = dialog.get_task_name()
            date = dialog.get_due_date()
            priority = dialog.get_priority()
            description = dialog.get_description()
            sub_tasks = dialog.get_subtasks()
            selected_list_index = dialog.get_selected_list_index()
            
            # Добавляем задачу в интерфейс списка
            self.add_task_to_layout(task_name, date, priority, description, sub_tasks, self.tasks_layout.count() + 1)
            
            # Добавляем задачу в интерфейс всех задач
            task_card = TaskCard(task_name, date, priority, description, sub_tasks, self.all_tasks_layout.count() + 1, self)
            self.all_tasks_layout.addWidget(task_card)
            
            # Сохраняем задачу в JSON
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Получаем выбранный список задач
                task_list = data[selected_list_index]
                
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

    def load_lists(self):
        # Очищаем текущий layout
        while self.ui.tasks_layout_3.count():
            item = self.ui.tasks_layout_3.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                for list_item in data:
                    # Подсчитываем количество невыполненных задач
                    uncompleted_task_count = 0
                    for task in list_item['tasks']:
                        if not task['task_is_done']:
                            uncompleted_task_count += 1

                    # Создаем карточку списка
                    list_card = ListCard(
                        list_item['list_name'],
                        uncompleted_task_count,
                        data.index(list_item),
                        self, # Передаем экземпляр MainWindow
                        self.ui.tasks_container_3 # Родительский виджет для иерархии
                    )
                    
                    # Добавляем карточку в layout
                    self.ui.tasks_layout_3.addWidget(list_card)
                    
        except Exception as e:
            print(f"Ошибка при загрузке списков: {e}")

    def open_list(self, list_card):
        # Получаем индекс списка из свойства карточки
        list_index = list_card.list_index
        
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                if 0 <= list_index < len(data):
                    # Очищаем текущие задачи
                    while self.tasks_layout.count():
                        item = self.tasks_layout.takeAt(0)
                        if item.widget():
                            item.widget().deleteLater()
                    
                    # Устанавливаем название списка
                    self.ui.list_text.setText(data[list_index]['list_name'])
                    
                    # Создаем списки для выполненных и невыполненных задач
                    completed_tasks = []
                    uncompleted_tasks = []
                    
                    # Загружаем задачи из выбранного списка
                    for task in data[list_index]['tasks']:
                        # Форматируем подзадачи в строку
                        subtasks_text = ""
                        if task['task_subtasks']:
                            subtasks_text = "; ".join([subtask['subtask_name'] for subtask in task['task_subtasks']])
                        
                        # Создаем карточку задачи
                        task_card = TaskCard(
                            task['task_name'],
                            task['task_due_date'],
                            task['task_priority'],
                            task['task_description'],
                            subtasks_text,
                            task['id'],
                            self
                        )
                        
                        # Если задача выполнена, отмечаем её как выполненную
                        if task['task_is_done']:
                            task_card.checkbox.setChecked(True)
                            task_card.task_name.setStyleSheet("text-decoration: line-through; color: #666666;")
                            # Отмечаем все подзадачи как выполненные
                            for i in range(task_card.subtasks_layout.count()):
                                widget = task_card.subtasks_layout.itemAt(i).widget()
                                if widget:
                                    checkbox = widget.findChild(QCheckBox)
                                    label = widget.findChild(QLabel)
                                    if checkbox and label:
                                        checkbox.setChecked(True)
                                        label.setStyleSheet("text-decoration: line-through; color: #666666;")
                            completed_tasks.append(task_card)
                        else:
                            uncompleted_tasks.append(task_card)
                    
                    # Сначала добавляем невыполненные задачи
                    for task_card in uncompleted_tasks:
                        self.tasks_layout.addWidget(task_card)
                    
                    # Затем добавляем выполненные задачи
                    for task_card in completed_tasks:
                        self.tasks_layout.addWidget(task_card)
                    
                    # Переключаемся на страницу списка
                    self.stacked_widget.setCurrentIndex(1)
                    
        except Exception as e:
            print(f"Ошибка при открытии списка: {e}")

    def load_all_tasks(self):
        # Очищаем текущий layout
        while self.all_tasks_layout.count():
            item = self.all_tasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                # Создаем списки для выполненных и невыполненных задач
                completed_tasks = []
                uncompleted_tasks = []
                
                for list_item in data:
                    for task in list_item['tasks']:
                        # Форматируем подзадачи в строку
                        subtasks_text = ""
                        if task['task_subtasks']:
                            subtasks_text = "; ".join([subtask['subtask_name'] for subtask in task['task_subtasks']])
                        
                        # Создаем карточку задачи
                        task_card = TaskCard(
                            task['task_name'],
                            task['task_due_date'],
                            task['task_priority'],
                            task['task_description'],
                            subtasks_text,
                            task['id'],
                            self
                        )
                        
                        # Если задача выполнена, отмечаем её как выполненную
                        if task['task_is_done']:
                            task_card.checkbox.setChecked(True)
                            task_card.task_name.setStyleSheet("text-decoration: line-through; color: #666666;")
                            # Отмечаем все подзадачи как выполненные
                            for i in range(task_card.subtasks_layout.count()):
                                widget = task_card.subtasks_layout.itemAt(i).widget()
                                if widget:
                                    checkbox = widget.findChild(QCheckBox)
                                    label = widget.findChild(QLabel)
                                    if checkbox and label:
                                        checkbox.setChecked(True)
                                        label.setStyleSheet("text-decoration: line-through; color: #666666;")
                            completed_tasks.append(task_card)
                        else:
                            uncompleted_tasks.append(task_card)
                
                # Сначала добавляем невыполненные задачи
                for task_card in uncompleted_tasks:
                    self.all_tasks_layout.addWidget(task_card)
                
                # Затем добавляем выполненные задачи
                for task_card in completed_tasks:
                    self.all_tasks_layout.addWidget(task_card)
                    
        except Exception as e:
            print(f"Ошибка при загрузке всех задач: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet = load_stylesheet('styles.qss')

    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())