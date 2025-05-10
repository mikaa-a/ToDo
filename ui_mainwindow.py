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
        Form.resize(895, 582)
        Form.setMaximumSize(QSize(1920, 1200))
        self.central_widget = QWidget(Form)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setGeometry(QRect(-10, 0, 1541, 921))
        self.central_widget.setMaximumSize(QSize(1920, 1200))
        self.content = QStackedWidget(self.central_widget)
        self.content.setObjectName(u"content")
        self.content.setGeometry(QRect(0, 0, 911, 581))
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
        self.tasks_scroll_area.setGeometry(QRect(40, 150, 771, 391))
        self.tasks_scroll_area.setWidgetResizable(True)
        self.tasks_container = QWidget()
        self.tasks_container.setObjectName(u"tasks_container")
        self.tasks_container.setGeometry(QRect(0, 0, 769, 389))
        self.verticalLayoutWidget = QWidget(self.tasks_container)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 771, 391))
        self.tasks_layout = QVBoxLayout(self.verticalLayoutWidget)
        self.tasks_layout.setObjectName(u"tasks_layout")
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.tasks_scroll_area.setWidget(self.tasks_container)
        self.layoutWidget1 = QWidget(self.list_page)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(40, 20, 861, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.list_text = QLabel(self.layoutWidget1)
        self.list_text.setObjectName(u"list_text")

        self.horizontalLayout.addWidget(self.list_text)

        self.add_task_btn = QPushButton(self.layoutWidget1)
        self.add_task_btn.setObjectName(u"add_task_btn")

        self.horizontalLayout.addWidget(self.add_task_btn)

        self.edit_list_btn = QPushButton(self.layoutWidget1)
        self.edit_list_btn.setObjectName(u"edit_list_btn")

        self.horizontalLayout.addWidget(self.edit_list_btn)

        self.horizontalLayoutWidget = QWidget(self.list_page)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(40, 90, 421, 51))
        self.sort_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.sort_layout.setSpacing(8)
        self.sort_layout.setObjectName(u"sort_layout")
        self.sort_layout.setContentsMargins(0, 0, 0, 0)
        self.priority_sort_select = QComboBox(self.horizontalLayoutWidget)
        self.priority_sort_select.setObjectName(u"priority_sort_select")

        self.sort_layout.addWidget(self.priority_sort_select)

        self.sort_btn = QPushButton(self.horizontalLayoutWidget)
        self.sort_btn.setObjectName(u"sort_btn")

        self.sort_layout.addWidget(self.sort_btn)

        self.content.addWidget(self.list_page)

        self.retranslateUi(Form)

        self.content.setCurrentIndex(1)


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
    # retranslateUi

