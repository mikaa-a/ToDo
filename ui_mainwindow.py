# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(895, 627)
        Form.setMaximumSize(QSize(1920, 1200))
        self.central_widget = QWidget(Form)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setGeometry(QRect(-10, 0, 1541, 921))
        self.central_widget.setMaximumSize(QSize(1920, 1200))
        self.content = QStackedWidget(self.central_widget)
        self.content.setObjectName(u"content")
        self.content.setGeometry(QRect(0, 0, 911, 631))
        self.no_lists_page = QWidget()
        self.no_lists_page.setObjectName(u"no_lists_page")
        self.layoutWidget = QWidget(self.no_lists_page)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(220, 190, 511, 211))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.no_lists_text = QLabel(self.layoutWidget)
        self.no_lists_text.setObjectName(u"no_lists_text")
        font = QFont()
        font.setFamilies([u"Google Sans"])
        self.no_lists_text.setFont(font)
        self.no_lists_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.no_lists_text)

        self.no_lists_questions = QLabel(self.layoutWidget)
        self.no_lists_questions.setObjectName(u"no_lists_questions")
        self.no_lists_questions.setFont(font)
        self.no_lists_questions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.no_lists_questions)

        self.add_list_btn = QPushButton(self.layoutWidget)
        self.add_list_btn.setObjectName(u"add_list_btn")
        self.add_list_btn.setFont(font)

        self.verticalLayout.addWidget(self.add_list_btn)

        self.my_lists_text = QLabel(self.no_lists_page)
        self.my_lists_text.setObjectName(u"my_lists_text")
        self.my_lists_text.setGeometry(QRect(40, 30, 509, 42))
        self.my_lists_text.setFont(font)
        self.content.addWidget(self.no_lists_page)
        self.list_page = QWidget()
        self.list_page.setObjectName(u"list_page")
        self.back_to_list_btn = QPushButton(self.list_page)
        self.back_to_list_btn.setObjectName(u"back_to_list_btn")
        self.back_to_list_btn.setGeometry(QRect(40, 60, 181, 21))
        self.tasks_scroll_area = QScrollArea(self.list_page)
        self.tasks_scroll_area.setObjectName(u"tasks_scroll_area")
        self.tasks_scroll_area.setGeometry(QRect(40, 160, 771, 391))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tasks_scroll_area.sizePolicy().hasHeightForWidth())
        self.tasks_scroll_area.setSizePolicy(sizePolicy)
        self.tasks_scroll_area.setWidgetResizable(True)
        self.tasks_container = QWidget()
        self.tasks_container.setObjectName(u"tasks_container")
        self.tasks_container.setGeometry(QRect(0, 0, 769, 389))
        sizePolicy.setHeightForWidth(self.tasks_container.sizePolicy().hasHeightForWidth())
        self.tasks_container.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QWidget(self.tasks_container)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, -20, 771, 421))
        self.tasks_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.tasks_layout.setObjectName(u"tasks_layout")
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.tasks_scroll_area.setWidget(self.tasks_container)
        self.layoutWidget1 = QWidget(self.list_page)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(40, 10, 861, 41))
        self.top_bar_layout = QHBoxLayout(self.layoutWidget1)
        self.top_bar_layout.setObjectName(u"top_bar_layout")
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.list_text = QLabel(self.layoutWidget1)
        self.list_text.setObjectName(u"list_text")

        self.top_bar_layout.addWidget(self.list_text)

        self.add_task_btn = QPushButton(self.layoutWidget1)
        self.add_task_btn.setObjectName(u"add_task_btn")

        self.top_bar_layout.addWidget(self.add_task_btn)

        self.edit_list_btn = QPushButton(self.layoutWidget1)
        self.edit_list_btn.setObjectName(u"edit_list_btn")

        self.top_bar_layout.addWidget(self.edit_list_btn)

        self.horizontalLayoutWidget = QWidget(self.list_page)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(40, 90, 421, 51))
        self.sort_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.sort_layout.setSpacing(8)
        self.sort_layout.setObjectName(u"sort_layout")
        self.sort_layout.setContentsMargins(0, 0, 0, 0)
        self.priority_sort_select = QComboBox(self.horizontalLayoutWidget)
        self.priority_sort_select.setObjectName(u"priority_sort_select")
        self.priority_sort_select.setEnabled(True)

        self.sort_layout.addWidget(self.priority_sort_select)

        self.sort_btn = QPushButton(self.horizontalLayoutWidget)
        self.sort_btn.setObjectName(u"sort_btn")

        self.sort_layout.addWidget(self.sort_btn)

        self.content.addWidget(self.list_page)
        self.focus_page = QWidget()
        self.focus_page.setObjectName(u"focus_page")
        self.horizontalLayoutWidget_2 = QWidget(self.focus_page)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(360, 540, 239, 51))
        self.menu = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.menu.setObjectName(u"menu")
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.all_task_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.all_task_btn.setObjectName(u"all_task_btn")

        self.menu.addWidget(self.all_task_btn)

        self.all_lists_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.all_lists_btn.setObjectName(u"all_lists_btn")

        self.menu.addWidget(self.all_lists_btn)

        self.focus_mode_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.focus_mode_btn.setObjectName(u"focus_mode_btn")

        self.menu.addWidget(self.focus_mode_btn)

        self.focus_mode = QLabel(self.focus_page)
        self.focus_mode.setObjectName(u"focus_mode")
        self.focus_mode.setGeometry(QRect(30, 20, 361, 41))
        self.task_selection = QLabel(self.focus_page)
        self.task_selection.setObjectName(u"task_selection")
        self.task_selection.setGeometry(QRect(30, 70, 321, 41))
        self.tasks_scroll_area_2 = QScrollArea(self.focus_page)
        self.tasks_scroll_area_2.setObjectName(u"tasks_scroll_area_2")
        self.tasks_scroll_area_2.setGeometry(QRect(30, 120, 771, 391))
        sizePolicy.setHeightForWidth(self.tasks_scroll_area_2.sizePolicy().hasHeightForWidth())
        self.tasks_scroll_area_2.setSizePolicy(sizePolicy)
        self.tasks_scroll_area_2.setWidgetResizable(True)
        self.tasks_container_2 = QWidget()
        self.tasks_container_2.setObjectName(u"tasks_container_2")
        self.tasks_container_2.setGeometry(QRect(0, 0, 769, 389))
        sizePolicy.setHeightForWidth(self.tasks_container_2.sizePolicy().hasHeightForWidth())
        self.tasks_container_2.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget_2 = QWidget(self.tasks_container_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, -20, 771, 421))
        self.tasks_layout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.tasks_layout_2.setObjectName(u"tasks_layout_2")
        self.tasks_layout_2.setContentsMargins(0, 0, 0, 0)
        self.tasks_scroll_area_2.setWidget(self.tasks_container_2)
        self.content.addWidget(self.focus_page)
        self.all_tasks = QWidget()
        self.all_tasks.setObjectName(u"all_tasks")
        self.all_tasks_scroll_area = QScrollArea(self.all_tasks)
        self.all_tasks_scroll_area.setObjectName(u"all_tasks_scroll_area")
        self.all_tasks_scroll_area.setGeometry(QRect(40, 170, 771, 391))
        sizePolicy.setHeightForWidth(self.all_tasks_scroll_area.sizePolicy().hasHeightForWidth())
        self.all_tasks_scroll_area.setSizePolicy(sizePolicy)
        self.all_tasks_scroll_area.setWidgetResizable(True)
        self.tasks_container_4 = QWidget()
        self.tasks_container_4.setObjectName(u"tasks_container_4")
        self.tasks_container_4.setGeometry(QRect(0, 0, 769, 389))
        sizePolicy.setHeightForWidth(self.tasks_container_4.sizePolicy().hasHeightForWidth())
        self.tasks_container_4.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget_4 = QWidget(self.tasks_container_4)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(0, -20, 771, 421))
        self.tasks_layout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.tasks_layout_4.setObjectName(u"tasks_layout_4")
        self.tasks_layout_4.setContentsMargins(0, 0, 0, 0)
        self.all_tasks_scroll_area.setWidget(self.tasks_container_4)
        self.all_task_text = QLabel(self.all_tasks)
        self.all_task_text.setObjectName(u"all_task_text")
        self.all_task_text.setGeometry(QRect(40, 20, 251, 51))
        self.horizontalLayoutWidget_4 = QWidget(self.all_tasks)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(40, 80, 421, 51))
        self.sort_layout_2 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.sort_layout_2.setSpacing(8)
        self.sort_layout_2.setObjectName(u"sort_layout_2")
        self.sort_layout_2.setContentsMargins(0, 0, 0, 0)
        self.priority_sort_select_2 = QComboBox(self.horizontalLayoutWidget_4)
        self.priority_sort_select_2.setObjectName(u"priority_sort_select_2")
        self.priority_sort_select_2.setEnabled(True)

        self.sort_layout_2.addWidget(self.priority_sort_select_2)

        self.sort_btn_2 = QPushButton(self.horizontalLayoutWidget_4)
        self.sort_btn_2.setObjectName(u"sort_btn_2")

        self.sort_layout_2.addWidget(self.sort_btn_2)

        self.add_task_2 = QPushButton(self.all_tasks)
        self.add_task_2.setObjectName(u"add_task_2")
        self.add_task_2.setGeometry(QRect(630, 30, 241, 41))
        self.content.addWidget(self.all_tasks)
        self.my_lists = QWidget()
        self.my_lists.setObjectName(u"my_lists")
        self.horizontalLayoutWidget_3 = QWidget(self.my_lists)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(40, 30, 841, 61))
        self.Layout_my_lists = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.Layout_my_lists.setObjectName(u"Layout_my_lists")
        self.Layout_my_lists.setContentsMargins(0, 0, 0, 0)
        self.my_lists_text_2 = QLabel(self.horizontalLayoutWidget_3)
        self.my_lists_text_2.setObjectName(u"my_lists_text_2")

        self.Layout_my_lists.addWidget(self.my_lists_text_2)

        self.add_list = QPushButton(self.horizontalLayoutWidget_3)
        self.add_list.setObjectName(u"add_list")

        self.Layout_my_lists.addWidget(self.add_list)

        self.lists_scroll_area = QScrollArea(self.my_lists)
        self.lists_scroll_area.setObjectName(u"lists_scroll_area")
        self.lists_scroll_area.setGeometry(QRect(40, 120, 771, 391))
        sizePolicy.setHeightForWidth(self.lists_scroll_area.sizePolicy().hasHeightForWidth())
        self.lists_scroll_area.setSizePolicy(sizePolicy)
        self.lists_scroll_area.setWidgetResizable(True)
        self.tasks_container_3 = QWidget()
        self.tasks_container_3.setObjectName(u"tasks_container_3")
        self.tasks_container_3.setGeometry(QRect(0, 0, 769, 389))
        sizePolicy.setHeightForWidth(self.tasks_container_3.sizePolicy().hasHeightForWidth())
        self.tasks_container_3.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget_3 = QWidget(self.tasks_container_3)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(0, -20, 771, 421))
        self.tasks_layout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.tasks_layout_3.setObjectName(u"tasks_layout_3")
        self.tasks_layout_3.setContentsMargins(0, 0, 0, 0)
        self.lists_scroll_area.setWidget(self.tasks_container_3)
        self.content.addWidget(self.my_lists)

        self.retranslateUi(Form)

        self.content.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.no_lists_text.setText(QCoreApplication.translate("Form", u"\u0423 \u0432\u0430\u0441 \u043d\u0435\u0442 \u0441\u043f\u0438\u0441\u043a\u043e\u0432", None))
        self.no_lists_questions.setText(QCoreApplication.translate("Form", u"\u0417\u0430\u043f\u043b\u0430\u043d\u0438\u0440\u0443\u0435\u043c \u0447\u0442\u043e \u043d\u0438\u0431\u0443\u0434\u044c?", None))
        self.add_list_btn.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.my_lists_text.setText(QCoreApplication.translate("Form", u"\u041c\u043e\u0438 \u0441\u043f\u0438\u0441\u043a\u0438", None))
        self.back_to_list_btn.setText(QCoreApplication.translate("Form", u"\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u043a\u043e \u0432\u0441\u0435\u043c \u0441\u043f\u0438\u0441\u043a\u0430\u043c", None))
        self.list_text.setText(QCoreApplication.translate("Form", u"\u0421\u043f\u0438\u0441\u043e\u043a 1", None))
        self.add_task_btn.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.edit_list_btn.setText(QCoreApplication.translate("Form", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.sort_btn.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.all_task_btn.setText(QCoreApplication.translate("Form", u"2", None))
        self.all_lists_btn.setText(QCoreApplication.translate("Form", u"2", None))
        self.focus_mode_btn.setText(QCoreApplication.translate("Form", u"2", None))
        self.focus_mode.setText(QCoreApplication.translate("Form", u"\u0420\u0435\u0436\u0438\u043c \u0444\u043e\u043a\u0443\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f", None))
        self.task_selection.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.all_task_text.setText(QCoreApplication.translate("Form", u"\u0412\u0441\u0435 \u0437\u0430\u0434\u0430\u0447\u0438", None))
        self.sort_btn_2.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.add_task_2.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u0434\u0430\u0447\u0443", None))
        self.my_lists_text_2.setText(QCoreApplication.translate("Form", u"\u041c\u043e\u0438 \u0441\u043f\u0438\u0441\u043a\u0438", None))
        self.add_list.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
    # retranslateUi

