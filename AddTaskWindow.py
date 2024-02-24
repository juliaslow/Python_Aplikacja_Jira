from datetime import datetime

from PySide6.QtCore import QDate, QTime, QDateTime
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, \
    QCalendarWidget, QTimeEdit, QMessageBox

from DataBaseHandler import DataBaseHandler


class AddTaskWindow(QDialog):
    def __init__(self,user_info):
        super().__init__()
        self.setWindowTitle("Dodaj nowe zadanie")
        layout = QVBoxLayout(self)
        self.setStyleSheet("""
                                   QPushButton {
                                       background-color: #4CAF50;
                                       border: none;
                                       color: white;
                                       padding: 3px 10px;
                                       text-align: center;
                                       text-decoration: none;
                                       font-size: 14px;
                                       margin: 4px 2px;
                                       cursor: pointer;
                                       border-radius: 8px;
                                   }

                                   QPushButton:hover {
                                       background-color: #45a049;
                                   }

                                   QPushButton:pressed {
                                       background-color: #3e8e41;
                                   }
                               """)
        self.user_info =user_info
        self.employee_combo_box = QComboBox()
        layout.addWidget(QLabel("<b>Wybierz pracownika:</b>"))
        layout.addWidget(self.employee_combo_box)
        self.dataBaseHandler = DataBaseHandler()
        if user_info['stanowisko'] == 'Manager':
            employees = self.dataBaseHandler.get_employees(user_info['stanowisko'],user_info['zespol'])
        else:
            employees = self.dataBaseHandler.get_employees(user_info['stanowisko'],user_info['jednostka'])

        for emp in employees:
            self.employee_combo_box.addItem(f"{emp['imie']} {emp['nazwisko']}", emp['id'])

        self.title_label = QLabel("<b>Tytuł:</b>")
        self.title_input = QLineEdit()

        self.description_label = QLabel("<b>Opis:</b>")
        self.description_input = QLineEdit()

        self.comments_label = QLabel("<b>Uwagi:</b>")
        self.comments_input = QLineEdit()

        self.deadline_label = QLabel("<b>Termin wykonania:</b>")
        self.deadline_input = QCalendarWidget()
        self.deadline_input.setSelectedDate(QDate.currentDate())

        self.deadlinetime_label = QLabel("<b>Godzina wykonania:</b>")
        self.deadlinetime_input = QTimeEdit()
        self.deadlinetime_input.setTime(QTime.currentTime())

        self.priority_label = QLabel("<b>Priorytet:</b>")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Niski", "Średni", "Wysoki"])

        self.status_label = QLabel("<b>Status:</b>")
        self.status_input = QComboBox()
        self.status_input.addItems(["Nowe", "W trakcie", "Zakończone"])

        self.add_button = QPushButton("Dodaj zadanie")
        self.add_button.clicked.connect(self.add_task_to_db)

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.comments_label)
        layout.addWidget(self.comments_input)
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)
        layout.addWidget(self.deadlinetime_label)
        layout.addWidget(self.deadlinetime_input)
        layout.addWidget(self.priority_label)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task_to_db(self):
        title = self.title_input.text()
        description = self.description_input.text()
        comments = self.comments_input.text()
        deadline_date = self.deadline_input.selectedDate().toString("yyyy-MM-dd")
        deadline_time = self.deadlinetime_input.time().toString("HH:mm")
        priority = self.priority_input.currentText()
        status = self.status_input.currentText()

        if not title:
            QMessageBox.warning(self, "Błąd", "Tytuł zadania jest wymagany.")
            return

        employee_id = self.employee_combo_box.currentData()
        deadline_datetime = QDateTime.fromString(deadline_date + " " + deadline_time, "yyyy-MM-dd HH:mm").toPython()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Dodaj zadanie do bazy danych
        db_handler = DataBaseHandler()
        db_handler.add_task(employee_id, self.user_info['id'], status, priority, title, description, comments,
                            current_datetime, deadline_datetime)
        QMessageBox.information(self, "Sukces", "Zadanie zostało dodane do bazy danych.")
        self.close()
