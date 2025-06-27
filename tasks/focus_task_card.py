from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QSizePolicy, QLayout
from PySide6.QtCore import Qt, QDate

class FocusTaskCard(QWidget):
    def __init__(self, text: str, date: str, priority: str, description: str, sub_tasks: str, task_id: int, parent=None):
        super().__init__()
        self.task_id = task_id
        self.parent = parent
        self.setObjectName("focus_task_card_widget")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setMinimumWidth(0)

        self.container = QFrame()
        self.container.setObjectName("focus_task_card")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.container.setMinimumWidth(0)
        self.container.setStyleSheet("background-color: #B1CCBB; border-radius: 16px;")

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(2)
        self.top_layout.setAlignment(Qt.AlignVCenter)

        # Убираем чекбокс - добавляем только отступ для выравнивания
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(20)  # Уменьшаем ширину отступа
        self.top_layout.addWidget(spacer_widget)

        self.task_name = QLabel(text)
        self.task_name.setObjectName("focus_task_name")
        self.task_name.setWordWrap(True)
        self.task_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.task_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.top_layout.addWidget(self.task_name)

        self.top_layout.addStretch()

        self.top_info = QLabel(f"{self.format_date(date)}  •  {self.get_priority_text(priority)}")
        self.top_info.setObjectName("focus_task_top_info")
        self.top_info.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.top_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.top_info.setStyleSheet("""margin-bottom: 10px""")
        self.top_layout.addWidget(self.top_info)

        self.main_layout.addLayout(self.top_layout)

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