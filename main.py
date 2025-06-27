import sys
import json
from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QCheckBox, QPushButton, QFrame, QMessageBox, QLayout, QComboBox, QSpacerItem
from PySide6.QtCore import QFile, Qt, QDate, QRect, QSize
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from ui_mainwindow import Ui_Form
from dialogs.add_task_dialog import AddTaskDialog
from dialogs.edit_list_dialog import EditListDialog
from dialogs.add_list_dialog import AddListDialog
from tasks.task_card import TaskCard, SubtaskWidget
from tasks.focus_task_card import FocusTaskCard
from utils.helpers import load_stylesheet
from datetime import datetime

class ListCard(QWidget):
    def __init__(self, list_name, uncompleted_task_count, list_index, main_window_instance, parent=None):
        super().__init__(parent)
        self.list_index = list_index
        self.main_window_instance = main_window_instance
        
        # Устанавливаем политику размеров для карточки
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(120)  # 100px + 4px отступ сверху + 4px отступ снизу + 8px внутренние отступы + 4px дополнительно
        self.setMaximumHeight(120)
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)  # Максимально возможная ширина
        
        # Основной layout для виджета
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Создаем контейнер для стилей
        self.container = QFrame()
        self.container.setObjectName("list_card_frame")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setMinimumWidth(0)
      
        
        # Основной layout для контейнера
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(12, 8, 12, 8)
        container_layout.setSpacing(15)
        
        # Создаем вертикальный layout для текста
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.setAlignment(Qt.AlignVCenter)
        
        # Добавляем название списка
        name_label = QLabel(list_name)
        name_label.setObjectName("list_name")
        name_label.setStyleSheet("font-size: 24px; font-weight: 500;")
        name_label.setWordWrap(True)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        name_label.setMinimumWidth(0)
        name_label.setMaximumWidth(16777215)
        text_layout.addWidget(name_label)
        
        # Добавляем количество невыполненных задач
        count_text = f"{uncompleted_task_count} {'невыполненная задача' if uncompleted_task_count == 1 else 'невыполненных задачи' if 1 < uncompleted_task_count < 5 else 'невыполненных задач'}"
        count_label = QLabel(count_text)
        count_label.setStyleSheet("font-size: 18px;")
        count_label.setObjectName("list_task_count")
        count_label.setWordWrap(True)
        count_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        count_label.setMinimumWidth(0)
        count_label.setMaximumWidth(16777215)
        text_layout.addWidget(count_label)
        
        container_layout.addLayout(text_layout)
        container_layout.addStretch()
        
        # Устанавливаем курсор в виде руки при наведении
        self.setCursor(Qt.PointingHandCursor)
        
        # Добавляем контейнер в основной layout
        main_layout.addWidget(self.container)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Вызываем метод open_list у экземпляра MainWindow
            self.main_window_instance.open_list(self)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(1000, 600)

        # Создаем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем главный лейаут для центрального виджета
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # Создаем контейнер для основного контента
        content_container = QWidget()
        content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.ui = Ui_Form()
        self.ui.setupUi(content_container)
        self.stacked_widget = self.ui.content

        for widget in self.findChildren(QLabel):
            widget.setStyleSheet(widget.styleSheet() + "font-family: 'Montserrat';")
        for widget in self.findChildren(QPushButton):
            widget.setStyleSheet(widget.styleSheet() + "font-family: 'Montserrat';")
            widget.setCursor(Qt.PointingHandCursor)
        for widget in self.findChildren(QComboBox):
            widget.setStyleSheet(widget.styleSheet() + "font-family: 'Montserrat';")

        # Удаляем старую геометрию content
        self.ui.content.setGeometry(QRect())
        self.ui.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Добавляем content в контейнер контента
        content_layout.addWidget(self.ui.content)

        # Добавляем контейнер контента в центральный лейаут
        self.central_layout.addWidget(content_container)

        # Создаем контейнер для меню
        self.menu_container = QWidget()
        self.menu_container.setObjectName("menu_container")
        self.menu_container.setFixedHeight(45)
        self.menu_container.setFixedWidth(235)
        
        # Создаем лейаут для меню
        menu_layout = QHBoxLayout(self.menu_container)
        menu_layout.setContentsMargins(30, 0, 50, 0)
        menu_layout.setSpacing(0)
        menu_layout.setAlignment(Qt.AlignCenter)
        
        # Настраиваем кнопки меню
        for button in [self.ui.all_task_btn, self.ui.all_lists_btn, self.ui.focus_mode_btn]:
            button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                    font-size: 18px;
                    color: #F3F2F3;
                    border-radius: 8px;
                }
            """)
            menu_layout.addWidget(button)
        
        # Создаем контейнер для центрирования меню в безопасной зоне
        menu_wrapper = QWidget()
        menu_wrapper.setObjectName("menu_wrapper")
        menu_wrapper_layout = QVBoxLayout(menu_wrapper)
        menu_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        
        # Создаем три равных пространства для вертикального распределения
        top_spacer = QWidget()
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        top_spacer.setMinimumHeight(0)
        
        middle_container = QWidget()
        middle_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        middle_layout = QVBoxLayout(middle_container)
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(0)
        
        # Создаем горизонтальный контейнер для центрирования меню
        menu_center_container = QWidget()
        menu_center_layout = QHBoxLayout(menu_center_container)
        menu_center_layout.setContentsMargins(0, 0, 0, 0)
        menu_center_layout.setSpacing(0)
        
        # Добавляем растягивающийся элемент слева
        menu_center_layout.addStretch()
        
        # Добавляем меню
        menu_center_layout.addWidget(self.menu_container)
        
        # Добавляем растягивающийся элемент справа
        menu_center_layout.addStretch()
        
        # Добавляем меню в средний контейнер
        middle_layout.addWidget(menu_center_container)
        
        bottom_spacer = QWidget()
        bottom_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bottom_spacer.setMinimumHeight(0)
        
        # Добавляем все элементы в основной layout с равными пропорциями
        menu_wrapper_layout.addWidget(top_spacer, 1)
        menu_wrapper_layout.addWidget(middle_container, 1)
        menu_wrapper_layout.addWidget(bottom_spacer, 1)
        
        # Добавляем обертку меню в центральный лейаут
        self.central_layout.addWidget(menu_wrapper)

        # Настраиваем страницу списка
        self.ui.list_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем страницу "Мои списки" для расширения
        self.ui.my_lists.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.lists_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tasks_container_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tasks_container_3.setMinimumWidth(0)
        
        # Настраиваем страницу "Режим фокусировки"
        self.ui.focus_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.focus_page.setMinimumHeight(400)
        
        # Сначала удаляем все дочерние виджеты со страницы фокусировки
        for child in self.ui.focus_page.findChildren(QWidget):
            if child != self.ui.focus_mode:  # Сохраняем только заголовок
                child.setParent(None)
                child.deleteLater()
        
        # Удаляем старый макет, если он существует
        if self.ui.focus_page.layout():
            old_layout = self.ui.focus_page.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
                    item.widget().deleteLater()
            QWidget().setLayout(old_layout)
        
        # Создаем макет для страницы фокусировки
        self.focus_page_layout = QVBoxLayout()
        self.focus_page_layout.setContentsMargins(38, 38, 38, 38)
        self.focus_page_layout.setSpacing(10)
        self.focus_page_layout.setAlignment(Qt.AlignTop)
        
        # Добавляем заголовок (если он еще не добавлен)
        if not self.ui.focus_mode.parent():
            self.ui.focus_mode.setObjectName("focus_mode")
            self.ui.focus_mode.setStyleSheet("font-size: 28px; font-weight: 600; color: #353028;")
            self.focus_page_layout.addWidget(self.ui.focus_mode)
        
        # Настраиваем область прокрутки
        self.ui.tasks_scroll_area_2 = QScrollArea(self.ui.focus_page)
        self.ui.tasks_scroll_area_2.setObjectName("tasks_scroll_area_2")
        self.ui.tasks_scroll_area_2.setWidgetResizable(True)
        self.ui.tasks_scroll_area_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.tasks_scroll_area_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tasks_scroll_area_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tasks_scroll_area_2.setMinimumWidth(600)
        self.ui.tasks_scroll_area_2.setMinimumHeight(0)
        self.ui.tasks_scroll_area_2.setStyleSheet("QScrollArea { background-color: #F3F2F3; border: none; }")
        
        # Создаем виджет для задач
        self.focus_tasks_widget = QWidget()
        self.focus_tasks_widget.setObjectName("focus_tasks_widget")
        self.focus_tasks_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.focus_tasks_widget.setStyleSheet("background-color: #F3F2F3; border: none;")
        
        # Создаем лейаут для задач
        self.focus_tasks_layout = QVBoxLayout(self.focus_tasks_widget)
        self.focus_tasks_layout.setAlignment(Qt.AlignTop)
        self.focus_tasks_layout.setSpacing(0) 
        self.focus_tasks_layout.setContentsMargins(0, 0, 0, 72)
        
        # Устанавливаем виджет задач в область прокрутки
        self.ui.tasks_scroll_area_2.setWidget(self.focus_tasks_widget)
        
        # Добавляем область прокрутки в макет страницы
        self.focus_page_layout.addSpacing(70)  # Увеличиваем отступ между заголовком и областью прокрутки
        self.focus_page_layout.addWidget(self.ui.tasks_scroll_area_2)
        
        # Устанавливаем макет для страницы фокусировки
        self.ui.focus_page.setLayout(self.focus_page_layout)

        # Создаем главный лейаут для страницы списка
        self.list_page_layout = QVBoxLayout(self.ui.list_page)
        self.list_page_layout.setContentsMargins(28, 28, 28, 28)
        self.list_page_layout.setSpacing(0)  # Уменьшаем расстояние между элементами с 10 до 5 пикселей

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
        self.ui.list_text.setStyleSheet("margin: 0; padding: 0; font-weight: 600;")  # Убираем все возможные отступы через стили
        
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
        
        # Добавляем точку-разделитель между кнопками
        dot_label = QLabel("•")
        dot_label.setObjectName("header_dot")
        dot_label.setStyleSheet("color: #666666; font-size: 16px; margin: 0 0px;")
        self.header_layout.addWidget(dot_label)
        
        self.header_layout.addWidget(self.ui.edit_list_btn)
        
        # Устанавливаем выравнивание по вертикали для кнопок
        self.ui.add_task_btn.setFixedHeight(self.ui.list_text.height())
        self.ui.edit_list_btn.setFixedHeight(self.ui.list_text.height())
        
        # Добавляем header_layout в главный лейаут
        self.list_page_layout.addLayout(self.header_layout)

        # Добавляем кнопку "Вернуться к спискам"
        self.ui.back_to_list_btn.setContentsMargins(0, -24, 0, 0)  # Убираем отступ снизу
        self.ui.back_to_list_btn.clicked.connect(self.show_all_lists_page)  # Добавляем обработчик
        self.list_page_layout.addWidget(self.ui.back_to_list_btn)
        self.list_page_layout.addSpacing(24)  # Добавляем отступ после кнопки

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
        self.list_page_layout.addSpacing(12)  # Добавляем отступ между сортировкой и задачами

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
        self.ui.priority_sort_select.addItems(["По возрастанию", "По убыванию"])
        self.ui.priority_sort_select.setCurrentIndex(1)  # По умолчанию "По убыванию"
        self.ui.sort_btn.setText("Применить")
        self.ui.sort_btn.clicked.connect(self.sort_tasks)
        
        # Настройка комбо бокса для всех задач
        self.ui.priority_sort_select_2.addItems(["По возрастанию", "По убыванию"])
        self.ui.priority_sort_select_2.setCurrentIndex(1)  # По умолчанию "По убыванию"
        self.ui.sort_btn_2.setText("Применить")
        self.ui.sort_btn_2.clicked.connect(self.sort_all_tasks)

        self.ui.add_task_btn.clicked.connect(self.show_add_task_dialog)
        self.ui.edit_list_btn.clicked.connect(self.show_edit_list_dialog)
        
        # Загружаем задачи при инициализации
        self.load_tasks_from_json()

        # Устанавливаем иконки для кнопок нижнего меню
        self.ui.all_task_btn.setIcon(QIcon("icons/all_tasks.png"))
        self.ui.all_lists_btn.setIcon(QIcon("icons/my_lists.png"))
        self.ui.focus_mode_btn.setIcon(QIcon("icons/focus_mode.png"))

        # Устанавливаем размер иконок
        icon_size = 32
        self.ui.all_task_btn.setIconSize(QSize(icon_size, icon_size))
        self.ui.all_lists_btn.setIconSize(QSize(icon_size, icon_size))
        self.ui.focus_mode_btn.setIconSize(QSize(icon_size, icon_size))

        # Очищаем текст с кнопок
        self.ui.all_task_btn.setText("")
        self.ui.all_lists_btn.setText("")
        self.ui.focus_mode_btn.setText("")

        # Настраиваем выравнивание иконок по центру
        for btn in [self.ui.all_task_btn, self.ui.all_lists_btn, self.ui.focus_mode_btn]:
            btn.setStyleSheet(btn.styleSheet() + "text-align: center;")

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
        self.my_lists_layout.setSpacing(10)  # Уменьшаем отступ с 20 до 10 пикселей

        # Настраиваем заголовок
        self.ui.horizontalLayoutWidget_3.setContentsMargins(0, 0, 0, 0)
        self.ui.horizontalLayoutWidget_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.ui.Layout_my_lists.setContentsMargins(0, 0, 0, 0)
        self.ui.Layout_my_lists.setSpacing(10)
        
        # Создаем горизонтальный макет для заголовка и кнопки
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        
        # Добавляем заголовок в левую часть
        header_layout.addWidget(self.ui.my_lists_text_2)
        
        # Добавляем растягивающийся элемент
        header_layout.addStretch()
        
        # Добавляем кнопку в правую часть
        header_layout.addWidget(self.ui.add_list)
        
        # Очищаем старый макет и добавляем новый
        while self.ui.Layout_my_lists.count():
            item = self.ui.Layout_my_lists.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Добавляем новый макет в основной контейнер
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        self.ui.Layout_my_lists.addWidget(header_widget)
        self.ui.Layout_my_lists.setAlignment(Qt.AlignTop)

        # Настраиваем область прокрутки списков
        self.ui.lists_scroll_area.setWidgetResizable(True)
        self.ui.lists_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.lists_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.lists_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.lists_scroll_area.setMinimumWidth(600)

        # Добавляем виджеты в макет с отступами
        self.my_lists_layout.addWidget(self.ui.horizontalLayoutWidget_3)
        self.my_lists_layout.addSpacing(-25)  # Отступ между заголовком и списками
        self.my_lists_layout.addWidget(self.ui.lists_scroll_area)

        # Удаляем ненужный виджет task_selection
        if hasattr(self.ui, 'task_selection'):
            self.ui.task_selection.deleteLater()
            self.ui.task_selection = None

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
        
        # ---------------------- ФОКУС ДЕТАЛИЗАЦИЯ ----------------------
        self.focus_detail_page = QWidget()
        self.focus_detail_page.setObjectName("focus_detail_page")
        self.focus_detail_layout = QVBoxLayout(self.focus_detail_page)
        self.focus_detail_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.focus_detail_layout.setContentsMargins(38, 38, 38, 38)
        self.focus_detail_layout.setSpacing(2)
        FOCUS_DETAIL_PAGE_INDEX = 5
        self.ui.content.insertWidget(FOCUS_DETAIL_PAGE_INDEX, self.focus_detail_page)

        # Очищаем ссылку на старый контейнер
        self.ui.tasks_container_4 = None

        # Подключаем обработчик для кнопки добавления списка
        self.ui.add_list.clicked.connect(self.show_add_list_dialog)

        # Настраиваем страницу "Мои списки"
        self.ui.my_lists.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Настраиваем существующий контейнер для списков
        self.ui.tasks_container_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tasks_container_3.setContentsMargins(0, 0, 0, 0)

        # Настраиваем лейаут для списков
        self.ui.tasks_layout_3.setContentsMargins(0, 10, 0, 10)  # Добавляем отступы сверху и снизу
        self.ui.tasks_layout_3.setSpacing(10)
        self.ui.tasks_layout_3.setAlignment(Qt.AlignTop)

        # Удаляем старый виджет с отрицательным отступом
        if hasattr(self.ui, 'verticalLayoutWidget_3'):
            self.ui.verticalLayoutWidget_3.deleteLater()
            self.ui.verticalLayoutWidget_3 = None

        # Устанавливаем лейаут напрямую в контейнер
        self.ui.tasks_container_3.setLayout(self.ui.tasks_layout_3)

        # После полной инициализации интерфейса устанавливаем курсор для всех кнопок
        self.set_hand_cursor_for_all_buttons()

        # Открываем экран 'Мои списки' при запуске
        self.show_all_lists_page()

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
                    tasks = []
                    for task in first_list['tasks']:
                        # Форматируем подзадачи в строку
                        subtasks_text = ""
                        if task['task_subtasks']:
                            subtasks_text = "; ".join([subtask['subtask_name'] for subtask in task['task_subtasks']])
                        # Добавляем задачу в список для сортировки
                        tasks.append((task, subtasks_text))
                    # Сортировка по убыванию приоритета, если выбран этот пункт
                    if self.ui.priority_sort_select.currentText() == "По убыванию":
                        tasks.sort(key=lambda x: int(x[0]['task_priority']), reverse=True)
                    for task, subtasks_text in tasks:
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
            # Получаем имя текущего списка
            list_name = self.ui.list_text.text()
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                # Находим индекс списка по имени
                index_to_remove = next((i for i, l in enumerate(data) if l['list_name'] == list_name), None)
                if index_to_remove is not None:
                    del data[index_to_remove]
                    # Сохраняем обновленные данные
                    with open('data.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                # Очищаем layout задач
                while self.tasks_layout.count():
                    item = self.tasks_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                if hasattr(self, '_empty_list_widget'):
                    self._empty_list_widget = None
                # Если списки остались, показать первый, иначе сбросить заголовок
                if data:
                    self.ui.list_text.setText(data[0]['list_name'])
                    self.open_list(ListCard(data[0]['list_name'], 0, 0, self))
                else:
                    self.ui.list_text.setText("")
                    self.current_list_card = None
                # Обновить отображение всех списков
                self.load_lists()
                # После удаления сразу отправляем на страницу всех списков
                self.show_all_lists_page()
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
        
        # Добавляем задачи обратно в layout
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
        # Применяем сортировку по умолчанию
        if self.ui.priority_sort_select_2.currentText() == "По убыванию":
            self.sort_all_tasks()

        # Проверяем, есть ли задачи
        tasks_count = self.all_tasks_layout.count()
        if tasks_count == 0:
            # Скрываем фильтры и кнопку добавления
            self.ui.priority_sort_select_2.hide()
            self.ui.sort_btn_2.hide()
            self.ui.add_task_2.hide()

            # Если уже есть виджет пустого экрана — не добавляем второй раз
            if not hasattr(self, 'empty_all_tasks_widget'):
                self.empty_all_tasks_widget = QWidget()
                outer_layout = QVBoxLayout(self.empty_all_tasks_widget)
                self.empty_all_tasks_widget.setStyleSheet("margin-left: 45px")
                outer_layout.setContentsMargins(0, 0, 0, 0)
                outer_layout.setSpacing(0)
                outer_layout.addStretch(1)

                center_widget = QWidget()
                center_layout = QVBoxLayout(center_widget)
                center_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                center_layout.setSpacing(16)
                center_layout.setContentsMargins(0, 0, 0, 0)

                title = QLabel("У вас нет задач")
                title.setStyleSheet("font-size: 28px; font-weight: 600; color: #353028; margin-top: 60px;")
                title.setAlignment(Qt.AlignCenter)
                center_layout.addWidget(title)

                subtitle = QLabel("Запланируем что нибудь?")
                subtitle.setStyleSheet("font-size: 18px; color: #666666; margin-top: -4px;")
                subtitle.setAlignment(Qt.AlignCenter)
                center_layout.addWidget(subtitle)

                add_btn = QPushButton("Добавить задачу")
                add_btn.setStyleSheet("background-color: #6C946D; color: white; border-radius: 8px; padding: 10px 32px; font-size: 18px; font-weight: 500;")
                add_btn.setCursor(Qt.PointingHandCursor)
                center_layout.addWidget(add_btn, alignment=Qt.AlignHCenter)
                add_btn.clicked.connect(self.show_add_task_from_all_tasks_empty)

                outer_layout.addWidget(center_widget, alignment=Qt.AlignHCenter)
                outer_layout.addStretch(1)

                self.all_tasks_layout.addWidget(self.empty_all_tasks_widget)
        else:
            # Показываем фильтры и кнопку добавления
            self.ui.priority_sort_select_2.show()
            self.ui.sort_btn_2.show()
            self.ui.add_task_2.show()
            # Удаляем виджет пустого экрана, если он был
            if hasattr(self, 'empty_all_tasks_widget') and self.empty_all_tasks_widget is not None:
                self.empty_all_tasks_widget.setParent(None)
                self.empty_all_tasks_widget = None

    def show_add_task_from_all_tasks_empty(self):
        dialog = AddTaskDialog(self, from_all_tasks=True)
        if dialog.exec() == QDialog.Accepted:
            selected_list_index = dialog.get_selected_list_index()
            if selected_list_index is None or selected_list_index < 0:
                QMessageBox.warning(self, "Ошибка", "Выберите список для задачи")
                return
            task_name = dialog.get_task_name()
            date = dialog.get_due_date()
            priority = dialog.get_priority()
            description = dialog.get_description()
            sub_tasks = dialog.get_subtasks()
            # Добавляем задачу в интерфейс всех задач
            task_card = TaskCard(task_name, date, priority, description, sub_tasks, 1, self)
            self.all_tasks_layout.addWidget(task_card)
            # Сохраняем задачу в JSON
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                task_list = data[selected_list_index]
                new_task = {
                    "id": len(task_list['tasks']) + 1,
                    "task_name": task_name,
                    "task_description": description,
                    "task_priority": priority,
                    "task_due_date": date,
                    "task_is_done": False,
                    "task_subtasks": []
                }
                if sub_tasks:
                    subtasks_list = [subtask.strip() for subtask in sub_tasks.split(';') if subtask.strip()]
                    for i, subtask in enumerate(subtasks_list, 1):
                        new_task["task_subtasks"].append({
                            "id": i,
                            "subtask_name": subtask,
                            "is_completed": False
                        })
                task_list['tasks'].append(new_task)
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                # После добавления задачи обновляем страницу
                self.show_all_tasks_page()
            except Exception as e:
                print(f"Ошибка при сохранении задачи: {e}")

    def show_all_lists_page(self):
        self.stacked_widget.setCurrentIndex(4)  # Переключаем на страницу списков
        self.load_lists()  # Загружаем списки

    def show_focus_page(self):
        # если какая-то задача уже is_focused=True – открываем её сразу
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for lst in data:
                for t in lst['tasks']:
                    if t.get('is_focused'):
                        self.build_focus_detail_page(t, lst['list_name'])
                        self.stacked_widget.setCurrentIndex(5)
                        return
        except Exception:
            pass
        # иначе обычный список задач
        self.stacked_widget.setCurrentIndex(2)
        self.load_focus_tasks()

    def load_focus_tasks(self):
        # Чистим текущий layout
        while self.focus_tasks_layout.count():
            item = self.focus_tasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            uncompleted_tasks, completed_tasks = [], []
            for task_list in data:                                  # каждый список в файле
                list_name = task_list['list_name']
                for task in task_list['tasks']:                     # каждая задача
                    # собираем подзадачи в строку
                    subtasks_text = "; ".join(
                        sub['subtask_name'] for sub in task['task_subtasks']
                    ) if task['task_subtasks'] else ""
                    # создаём специальную карточку для режима фокусировки
                    card = FocusTaskCard(
                        task['task_name'],
                        task['task_due_date'],
                        task['task_priority'],
                        task['task_description'],
                        subtasks_text,
                        task['id'],
                        self
                    )
                    card.mousePressEvent = (
                        lambda e, tid=task['id'], lname=list_name:
                            self.open_focus_task(tid, lname) if e.button() == Qt.LeftButton else None
                    )
                    # распределяем по спискам
                    if task['task_is_done']:
                        completed_tasks.append(card)
                    else:
                        uncompleted_tasks.append(card)
            # сортируем – приоритет берём так же, как в get_priority_value
            def prio(card_widget):
                text = card_widget.top_info.text().split(' • ')[1].strip()
                return self.get_priority_value(text)
            uncompleted_tasks.sort(key=prio, reverse=True)
            # completed_tasks.sort(key=prio, reverse=True)
            
            # Проверяем, есть ли незавершенные задачи
            if len(uncompleted_tasks) == 0:
                # Создаем виджет пустого экрана для фокусировки
                empty_focus_widget = QWidget()
                outer_layout = QVBoxLayout(empty_focus_widget)
                outer_layout.setContentsMargins(0, 0, 0, 0)
                outer_layout.setSpacing(0)
                outer_layout.addStretch(1)

                center_widget = QWidget()
                center_layout = QVBoxLayout(center_widget)
                center_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                center_layout.setSpacing(16)
                center_layout.setContentsMargins(0, 0, 0, 0)

                title = QLabel("Нет незавершенных задач")
                title.setStyleSheet("font-size: 28px; font-weight: 600; color: #353028; margin-top: 60px;")
                title.setAlignment(Qt.AlignCenter)
                center_layout.addWidget(title)

                outer_layout.addWidget(center_widget, alignment=Qt.AlignHCenter)
                outer_layout.addStretch(1)

                self.focus_tasks_layout.addWidget(empty_focus_widget)
            else:
                for card in uncompleted_tasks:
                    self.focus_tasks_layout.addWidget(card)
            # for card in uncompleted_tasks + completed_tasks:
            #     self.focus_tasks_layout.addWidget(card)
        except Exception as e:
            print(f"Ошибка при загрузке задач в режиме фокусировки: {e}")

    def build_focus_detail_page(self, task_dict, list_name):
        from tasks.task_card import SubtaskWidget
        # Минимальный spacing для основного layout
        self.focus_detail_layout.setSpacing(2)
        while self.focus_detail_layout.count():
            item = self.focus_detail_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        # --- название задачи ---
        title = QLabel(task_dict['task_name'])
        title.setStyleSheet("font-size: 28px; font-weight: 600; color: #353028; padding: 0; margin-left: -4px")
        title.setAlignment(Qt.AlignLeft)
        title.setWordWrap(True)
        self.focus_detail_layout.addWidget(title)
        self.focus_detail_layout.addSpacing(8)  # Меньше расстояние после названия
        # --- описание (без скролла, обычный QLabel, переносится до конца экрана) ---
        desc = QLabel(task_dict.get('task_description', ''))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 16px; color: #353028; padding: 0;")
        desc.setAlignment(Qt.AlignLeft)
        desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.focus_detail_layout.addWidget(desc)
        self.focus_detail_layout.addSpacing(18)  # Большее расстояние после описания
        # --- подзадачи ----
        if task_dict['task_subtasks']:
            subtasks_container = QWidget()
            subtasks_layout = QVBoxLayout(subtasks_container)
            subtasks_layout.setContentsMargins(0, 0, 0, 0)
            subtasks_layout.setSpacing(6)  # минимальное расстояние между подзадачами
            for sub in task_dict['task_subtasks']:
                subtask_widget = SubtaskWidget(sub['subtask_name'])
                subtask_widget.setFixedHeight(22)
                subtask_widget.checkbox.setChecked(sub['is_completed'])
                # subtask_widget.checkbox.setEnabled(False)  # теперь чекбокс активен
                # Подключаем обработчик клика
                subtask_widget.checkbox.clicked.connect(
                    lambda checked, w=subtask_widget, sid=task_dict['id'], lname=list_name, sname=sub['subtask_name']:
                        self.handle_focus_subtask_click(checked, w, sid, lname, sname)
                )
                subtasks_layout.addWidget(subtask_widget)
            # Ограниченная область с прокруткой только для подзадач
            from PySide6.QtWidgets import QScrollArea
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll.setMinimumHeight(40)
            scroll.setMaximumHeight(100)
            scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
            subtasks_container.setStyleSheet("background: transparent;")
            scroll.setWidget(subtasks_container)
            self.focus_detail_layout.addWidget(scroll)
            self.focus_detail_layout.addSpacing(18)  # Большее расстояние после подзадач
        else:
            self.focus_detail_layout.addSpacing(8)  # Если нет подзадач, чуть меньше
        # --- время старта ---
        start_lbl = QLabel(f"Начата {task_dict.get('start_time', '')}")
        start_lbl.setStyleSheet("font-size: 14px; color: #666666; padding: 0;")
        start_lbl.setAlignment(Qt.AlignLeft)
        self.focus_detail_layout.addWidget(start_lbl)
        self.focus_detail_layout.addSpacing(1)
        # --- кнопки ---
        self.focus_detail_layout.addStretch(1)  # Кнопки всегда внизу
        row_btns = QWidget()
        row_lay = QHBoxLayout(row_btns)
        row_lay.setAlignment(Qt.AlignLeft)
        row_lay.setSpacing(10)
        row_lay.setContentsMargins(0, 0, 0, 0)
        exit_btn = QPushButton("Выйти из фокусирования")
        exit_btn.setStyleSheet("background-color:#4C4C4C;color:#FFFFFF;border-radius:8px;"
                               "padding:6px 10px;font-size:13px;")
        finish_btn = QPushButton("Завершить задачу")
        finish_btn.setStyleSheet("background-color:#6C946D;color:#FFFFFF;border-radius:8px;"
                                 "padding:6px 10px;font-size:13px;")
        row_lay.addWidget(exit_btn)
        row_lay.addWidget(finish_btn)
        self.focus_detail_layout.addWidget(row_btns)
        exit_btn.clicked.connect(self.exit_focus_task)
        finish_btn.clicked.connect(lambda: self.finish_focus_task(task_dict['id'], list_name))
        row_btns.setStyleSheet("""margin-bottom: 40px""")

    def open_focus_task(self, task_id, list_name):
        """Помечает задачу как is_focused=True, проставляет start_time и переводит на детальную страницу."""
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            # сбрасываем предыдущий фокус
            for lst in data:
                for t in lst['tasks']:
                    t['is_focused'] = False
            target = None
            for lst in data:
                if lst['list_name'] == list_name:
                    for t in lst['tasks']:
                        if t['id'] == task_id:
                            t['is_focused'] = True
                            now = datetime.now()
                            months = ["января","февраля","марта","апреля","мая","июня",
                                      "июля","августа","сентября","октября","ноября","декабря"]
                            t['start_time'] = f"{now.day} {months[now.month-1]} {now.year} в {now.strftime('%H:%M')}"
                            target = t
                            break
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            if target:
                self.build_focus_detail_page(target, list_name)
                self.stacked_widget.setCurrentIndex(5)
        except Exception as e:
            print(f"Ошибка при открытии фокус-задачи: {e}")

    def exit_focus_task(self):
        """Сброс фокуса без завершения задачи."""
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for lst in data:
                for t in lst['tasks']:
                    t['is_focused'] = False
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass
        self.show_focus_page()

    def finish_focus_task(self, task_id, list_name):
        """Помечает задачу как выполненную и сбрасывает фокус."""
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            for lst in data:
                if lst['list_name'] == list_name:
                    for t in lst['tasks']:
                        if t['id'] == task_id:
                            t['task_is_done'] = True
                            t['is_focused'] = False
                            break
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при завершении задачи: {e}")
        self.show_focus_page()

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
        
        # Добавляем задачи обратно в layout
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
        widgets_to_remove = []
        for i in range(self.ui.tasks_layout_3.count()):
            item = self.ui.tasks_layout_3.itemAt(i)
            widget = item.widget()
            if widget and (not hasattr(self, 'empty_lists_widget') or widget != self.empty_lists_widget):
                widgets_to_remove.append(widget)
        for widget in widgets_to_remove:
            self.ui.tasks_layout_3.removeWidget(widget)
            widget.deleteLater()

        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

                if len(data) == 0:
                    # Пустой экран для "Мои списки"
                    self.ui.add_list.hide()
                    # Удаляем старый пустой экран, если он есть
                    if hasattr(self, 'empty_lists_widget') and self.empty_lists_widget is not None:
                        self.empty_lists_widget.setParent(None)
                        self.empty_lists_widget.deleteLater()
                        self.empty_lists_widget = None
                    # Создаём новый пустой экран
                    self.empty_lists_widget = QWidget()
                    outer_layout = QVBoxLayout(self.empty_lists_widget)
                    self.empty_lists_widget.setStyleSheet("margin-left: 45px")
                    outer_layout.setContentsMargins(0, 0, 0, 0)
                    outer_layout.setSpacing(0)
                    outer_layout.addStretch(1)
                    center_widget = QWidget()
                    center_layout = QVBoxLayout(center_widget)
                    center_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    center_layout.setSpacing(16)
                    center_layout.setContentsMargins(0, 0, 0, 0)
                    title = QLabel("У вас нет списков")
                    title.setStyleSheet("font-size: 28px; font-weight: 600; color: #353028;")
                    title.setAlignment(Qt.AlignCenter)
                    center_layout.addWidget(title)
                    subtitle = QLabel("Запланируем что нибудь?")
                    subtitle.setStyleSheet("font-size: 18px; color: #666666; margin-top: -4px;")
                    subtitle.setAlignment(Qt.AlignCenter)
                    center_layout.addWidget(subtitle)
                    add_btn = QPushButton("Добавить список")
                    add_btn.setStyleSheet("background-color: #6C946D; color: white; border-radius: 8px; padding: 10px 32px; font-size: 18px; font-weight: 500; margin-bottom: 50px;")
                    add_btn.setCursor(Qt.PointingHandCursor)
                    center_layout.addWidget(add_btn, alignment=Qt.AlignHCenter)
                    add_btn.clicked.connect(self.show_add_list_dialog)
                    outer_layout.addWidget(center_widget, alignment=Qt.AlignHCenter)
                    outer_layout.addStretch(1)
                    self.ui.tasks_layout_3.addWidget(self.empty_lists_widget)
                else:
                    self.ui.add_list.show()
                    # Удаляем пустой экран, если он был
                    if hasattr(self, 'empty_lists_widget') and self.empty_lists_widget is not None:
                        self.empty_lists_widget.setParent(None)
                        self.empty_lists_widget = None

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
                        self,
                        self.ui.tasks_container_3
                    )
                    # Добавляем карточку в layout
                    self.ui.tasks_layout_3.addWidget(list_card)
        except Exception as e:
            print(f"Ошибка при загрузке списков: {e}")

    def open_list(self, list_card):
        # Проверяем, что список существует и индекс валиден
        if not hasattr(list_card, 'list_index'):
            self.current_list_card = None
            return
        list_index = list_card.list_index
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        if not (0 <= list_index < len(data)):
            self.current_list_card = None
            return
        # Сохраняем текущий выбранный список
        self.current_list_card = list_card
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
                    
                    # Сортировка по убыванию приоритета, если выбран этот пункт
                    if self.ui.priority_sort_select.currentText() == "По убыванию":
                        uncompleted_tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()), reverse=True)
                        completed_tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()), reverse=True)
                    # Сначала добавляем невыполненные задачи
                    for task_card in uncompleted_tasks:
                        self.tasks_layout.addWidget(task_card)
                    # Затем добавляем выполненные задачи
                    for task_card in completed_tasks:
                        self.tasks_layout.addWidget(task_card)
                    
                    # Если задач нет вообще, показать блок с уведомлением и кнопкой
                    if not uncompleted_tasks and not completed_tasks:
                        # Скрываем сортировку, кнопку добавления задачи и точку-разделитель
                        self.ui.priority_sort_select.hide()
                        self.ui.sort_btn.hide()
                        self.ui.add_task_btn.hide()
                        header_dot = self.findChild(QLabel, "header_dot")
                        if header_dot:
                            header_dot.hide()
                        # Удаляем старый блок уведомления, если он есть
                        if hasattr(self, '_empty_list_widget') and self._empty_list_widget is not None:
                            self._empty_list_widget.setParent(None)
                            self._empty_list_widget.deleteLater()
                            self._empty_list_widget = None
                        # Создаём новый блок уведомления
                        empty_list_widget = QWidget()
                        self._empty_list_widget = empty_list_widget
                        outer_layout = QVBoxLayout(empty_list_widget)
                        outer_layout.setContentsMargins(35, 50, 0, 0)
                        outer_layout.setSpacing(0)
                        outer_layout.addStretch(1)

                        center_widget = QWidget()
                        center_layout = QVBoxLayout(center_widget)
                        center_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        center_layout.setSpacing(16)
                        center_layout.setContentsMargins(0, 0, 0, 0)

                        title = QLabel("У вас нет задач")
                        title.setStyleSheet("font-size: 28px; font-weight: 600; color: #353028;")
                        title.setAlignment(Qt.AlignCenter)
                        center_layout.addWidget(title)

                        subtitle = QLabel("Запланируем что нибудь?")
                        subtitle.setStyleSheet("font-size: 18px; color: #666666; margin-top: -4px;")
                        subtitle.setAlignment(Qt.AlignCenter)
                        center_layout.addWidget(subtitle)

                        add_btn = QPushButton("Добавить задачу")
                        add_btn.setStyleSheet("background-color: #6C946D; color: white; border-radius: 8px; padding: 10px 32px; font-size: 18px; font-weight: 500;")
                        add_btn.setCursor(Qt.PointingHandCursor)
                        center_layout.addWidget(add_btn, alignment=Qt.AlignHCenter)
                        def open_add_task():
                            dialog = AddTaskDialog(self)
                            if dialog.exec() == QDialog.Accepted:
                                task_name = dialog.get_task_name()
                                date = dialog.get_due_date()
                                priority = dialog.get_priority()
                                description = dialog.get_description()
                                sub_tasks = dialog.get_subtasks()
                                self.add_task_to_layout(task_name, date, priority, description, sub_tasks, self.tasks_layout.count() + 1)
                                # Сохраняем задачу в JSON
                                try:
                                    with open('data.json', 'r', encoding='utf-8') as file:
                                        data = json.load(file)
                                    # Получаем текущий список
                                    list_name = self.ui.list_text.text()
                                    task_list = next((l for l in data if l['list_name'] == list_name), None)
                                    if task_list is not None:
                                        new_task = {
                                            "id": len(task_list['tasks']) + 1,
                                            "task_name": task_name,
                                            "task_description": description,
                                            "task_priority": priority,
                                            "task_due_date": date,
                                            "task_is_done": False,
                                            "task_subtasks": []
                                        }
                                        if sub_tasks:
                                            subtasks_list = [subtask.strip() for subtask in sub_tasks.split(';') if subtask.strip()]
                                            for i, subtask in enumerate(subtasks_list, 1):
                                                new_task["task_subtasks"].append({
                                                    "id": i,
                                                    "subtask_name": subtask,
                                                    "is_completed": False
                                                })
                                        task_list['tasks'].append(new_task)
                                        with open('data.json', 'w', encoding='utf-8') as file:
                                            json.dump(data, file, ensure_ascii=False, indent=4)
                                        # После добавления задачи обновить список
                                        self.open_list(list_card)
                                except Exception as e:
                                    print(f"Ошибка при сохранении задачи: {e}")
                        add_btn.clicked.connect(open_add_task)

                        outer_layout.addWidget(center_widget, alignment=Qt.AlignHCenter)
                        outer_layout.addStretch(1)
                        self.tasks_layout.addWidget(empty_list_widget)
                    else:
                        # Показываем сортировку, кнопку добавления задачи и точку-разделитель
                        self.ui.priority_sort_select.show()
                        self.ui.sort_btn.show()
                        self.ui.add_task_btn.show()
                        header_dot = self.findChild(QLabel, "header_dot")
                        if header_dot:
                            header_dot.show()
                        # Удаляем блок уведомления, если он есть
                        if hasattr(self, '_empty_list_widget') and self._empty_list_widget is not None:
                            self._empty_list_widget.setParent(None)
                            self._empty_list_widget.deleteLater()
                            self._empty_list_widget = None

                    # Переключаемся на страницу списка
                    self.stacked_widget.setCurrentIndex(1)
                    
        except Exception as e:
            print(f"Ошибка при открытии списка: {e}")

    def load_all_tasks(self):
        # Очищаем текущий layout, но не удаляем empty_all_tasks_widget
        widgets_to_remove = []
        for i in range(self.all_tasks_layout.count()):
            item = self.all_tasks_layout.itemAt(i)
            widget = item.widget()
            if widget and (not hasattr(self, 'empty_all_tasks_widget') or widget != self.empty_all_tasks_widget):
                widgets_to_remove.append(widget)
        for widget in widgets_to_remove:
            self.all_tasks_layout.removeWidget(widget)
            widget.deleteLater()

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
                # Сортировка по убыванию приоритета, если выбран этот пункт
                if self.ui.priority_sort_select_2.currentText() == "По убыванию":
                    uncompleted_tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()), reverse=True)
                    completed_tasks.sort(key=lambda x: self.get_priority_value(x.top_info.text().split(' • ')[1].strip()), reverse=True)
                # Сначала добавляем невыполненные задачи
                for task_card in uncompleted_tasks:
                    self.all_tasks_layout.addWidget(task_card)
                # Затем добавляем выполненные задачи
                for task_card in completed_tasks:
                    self.all_tasks_layout.addWidget(task_card)
        except Exception as e:
            print(f"Ошибка при загрузке всех задач: {e}")

    def show_add_list_dialog(self):
        dialog = AddListDialog(self)
        if dialog.exec() == QDialog.Accepted:
            new_list_name = dialog.get_list_name()
            
            try:
                # Читаем текущие данные
                with open('data.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Создаем новый список
                new_list = {
                    "list_name": new_list_name,
                    "id": len(data) + 1,
                    "tasks": []
                }
                
                # Добавляем новый список в данные
                data.append(new_list)
                
                # Сохраняем обновленные данные
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                
                # Обновляем отображение списков
                self.load_lists()
                
            except Exception as e:
                print(f"Ошибка при добавлении списка: {e}")
                QMessageBox.critical(self, "Ошибка", "Не удалось добавить список")

    def set_hand_cursor_for_all_buttons(self):
        for btn in self.findChildren(QPushButton):
            btn.setCursor(Qt.PointingHandCursor)

    def handle_focus_subtask_click(self, checked, subtask_widget, task_id, list_name, subtask_name):
        """Обновляет статус подзадачи в data.json и стиль подписи."""
        subtask_widget.update_style()
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            for lst in data:
                if lst['list_name'] == list_name:
                    for task in lst['tasks']:
                        if task['id'] == task_id:
                            for sub in task['task_subtasks']:
                                if sub['subtask_name'] == subtask_name:
                                    sub['is_completed'] = checked
                                    break
                            break
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении статуса подзадачи (фокус): {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Загружаем разные начертания шрифта Montserrat
    font_files = {
        'Regular': 'fonts/Montserrat-Regular.ttf',
        'Medium': 'fonts/Montserrat-Medium.ttf',
        'SemiBold': 'fonts/Montserrat-SemiBold.ttf',
        'Bold': 'fonts/Montserrat-Bold.ttf',
        'Light': 'fonts/Montserrat-Light.ttf'
    }
    
    for weight, file_path in font_files.items():
        font_id = QFontDatabase.addApplicationFont(file_path)
        if font_id == -1:
            print(f"Ошибка загрузки шрифта Montserrat {weight}")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            if weight == 'Regular':
                app.setFont(QFont(font_family))
    
    stylesheet = load_stylesheet('styles.qss')

    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())