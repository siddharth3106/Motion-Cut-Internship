import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
    QStatusBar, QDateEdit, QTimeEdit, QStyleFactory, QGridLayout, QSpacerItem, QSizePolicy,
    QDateTimeEdit, QTableWidgetItem, QHeaderView, QCheckBox, QGroupBox
)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QColor, QIcon  # Added QIcon import
import matplotlib.pyplot as plt
import csv

# File to store expense data
data_file = "expenses.json"

# Load existing data or initialize an empty list
def load_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 900, 600)

        # Apply a colorful QSS style to make it look modern and attractive
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2f; /* Dark background */
                color: #f0f0f0; /* Light text color */
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 18px;
                color: #ffffff;
                padding: 10px;
            }
            QLineEdit, QComboBox, QDateEdit, QTimeEdit {
                background-color: #2d2f3d; /* Darker input background */
                color: white;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #3c8dbc; /* Border color for inputs */
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus {
                border: 1px solid #4CAF50; /* Focus border color */
            }
            QPushButton {
                background-color: #4CAF50; /* Green buttons */
                color: white;
                padding: 12px;
                font-size: 14px;
                border-radius: 6px;
                transition: background-color 0.3s;
                min-width: 150px;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #388E3C; /* Darker green on hover */
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
            }
            QTableWidget {
                background-color: #2d2f3d;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QTableWidgetItem {
                background-color: #2d2f3d;
                color: white;
                padding: 10px;
                text-align: center;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50; /* Highlight selected items in green */
            }
            QStatusBar {
                background-color: #212121;
                color: #ffffff;
                font-size: 12px;
            }
            QPushButton#addExpenseButton {
                background-color: #2196F3; /* Blue for 'Add Expense' */
            }
            QPushButton#viewExpenseButton {
                background-color: #FF9800; /* Orange for 'View Expenses' */
            }
            QPushButton#filterExpenseButton {
                background-color: #9C27B0; /* Purple for 'Filter Expenses' */
            }
        """)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Main layout (Responsive and minimal design)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(50, 30, 50, 30)  # Adding margin to left and right

        # Header
        header_label = QLabel("Expense Tracker")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        main_layout.addWidget(header_label)

        # Input form
        form_layout = QFormLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter description")

        # Enhanced Date Input (Date and Time)
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        self.date_input.setCalendarPopup(True)

        # Enhanced Time Input
        self.time_input = QTimeEdit(QTime.currentTime())
        self.time_input.setDisplayFormat("HH:mm:ss")

        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Transportation", "Entertainment", "Utilities", "Other"])

        form_layout.addRow("Amount (₹):", self.amount_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Time:", self.time_input)
        form_layout.addRow("Category:", self.category_input)

        # Adding space between widgets for better layout
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(spacer)

        # Buttons (Professional & Modern)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        add_expense_button = QPushButton("Add Expense")
        add_expense_button.setObjectName("addExpenseButton")
        add_expense_button.setIcon(QIcon("icons/add.png"))  # Corrected icon reference
        add_expense_button.clicked.connect(self.add_expense)

        view_expenses_button = QPushButton("View Expenses")
        view_expenses_button.setObjectName("viewExpenseButton")
        view_expenses_button.setIcon(QIcon("icons/view.png"))  # Corrected icon reference
        view_expenses_button.clicked.connect(self.view_expenses)

        filter_button = QPushButton("Filter Expenses")
        filter_button.setObjectName("filterExpenseButton")
        filter_button.setIcon(QIcon("icons/filter.png"))  # Corrected icon reference
        filter_button.clicked.connect(self.filter_expenses)

        button_layout.addWidget(add_expense_button)
        button_layout.addWidget(view_expenses_button)
        button_layout.addWidget(filter_button)

        # Adding button layout to the main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_expense(self):
        try:
            amount = float(self.amount_input.text())
            description = self.description_input.text().strip()
            date = self.date_input.text().strip()
            time = self.time_input.text().strip()
            category = self.category_input.currentText()

            if not description or not date:
                raise ValueError("All fields must be filled!")

            expense = {
                "amount": amount,
                "description": description,
                "date": date,
                "time": time,
                "category": category,
            }
            data.append(expense)
            save_data(data)

            self.amount_input.clear()
            self.description_input.clear()
            self.date_input.setDate(QDate.currentDate())
            self.time_input.setTime(QTime.currentTime())
            self.category_input.setCurrentIndex(0)

            self.statusBar.showMessage("Expense added successfully!", 3000)
        except ValueError as e:
            self.statusBar.showMessage(f"Error: {str(e)}", 3000)

    def view_expenses(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Expense Summary")
        dialog.setGeometry(150, 150, 800, 400)

        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Date", "Description", "Category", "Amount", "Time"])

        for row, expense in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(expense["date"]))
            table.setItem(row, 1, QTableWidgetItem(expense["description"]))
            table.setItem(row, 2, QTableWidgetItem(expense["category"]))
            table.setItem(row, 3, QTableWidgetItem(f"₹{expense['amount']:.2f}"))
            table.setItem(row, 4, QTableWidgetItem(expense["time"]))

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

    def filter_expenses(self):
        # Placeholder for filtering functionality
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec_())
