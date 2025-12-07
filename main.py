import sys
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLabel, QLineEdit, QSpinBox, QMessageBox,
                             QComboBox, QTextEdit)
from PyQt5.QtCore import Qt, QDateTime, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from database import init_database
from models import BookModel, UserModel, LoanModel
from datetime import datetime


STYLESHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    
    QTabWidget::pane {
        border: 1px solid #ddd;
    }
    
    QTabBar::tab {
        background-color: #e8e8e8;
        color: #333;
        padding: 8px 20px;
        border: 1px solid #ccc;
        border-bottom: none;
        border-radius: 4px 4px 0 0;
        margin-right: 2px;
        font-weight: bold;
    }
    
    QTabBar::tab:selected {
        background-color: #2c3e50;
        color: white;
    }
    
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 11px;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton:pressed {
        background-color: #1f618d;
    }
    
    QPushButton#deleteBtn {
        background-color: #e74c3c;
    }
    
    QPushButton#deleteBtn:hover {
        background-color: #c0392b;
    }
    
    QLineEdit, QSpinBox, QComboBox, QTextEdit {
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        padding: 6px;
        background-color: white;
        selection-background-color: #3498db;
    }
    
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {
        border: 2px solid #3498db;
    }
    
    QLabel {
        color: #2c3e50;
        font-weight: 500;
    }
    
    QTableWidget {
        border: 1px solid #bdc3c7;
        gridline-color: #ecf0f1;
        background-color: white;
    }
    
    QTableWidget::item {
        padding: 5px;
        border-right: 1px solid #ecf0f1;
        border-bottom: 1px solid #ecf0f1;
    }
    
    QTableWidget::item:selected {
        background-color: #3498db;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #34495e;
        color: white;
        padding: 6px;
        border: none;
        font-weight: bold;
    }
    
    QDialog {
        background-color: #f5f5f5;
    }
"""


class BookDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        self.book = book
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('معلومات الكتاب' if self.book else 'إضافة كتاب جديد')
        self.setGeometry(100, 100, 450, 350)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel('العنوان:')
        title_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setMinimumHeight(35)
        if self.book:
            self.title_input.setText(self.book['title'])
        layout.addWidget(self.title_input)
        
        author_label = QLabel('المؤلف:')
        author_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(author_label)
        self.author_input = QLineEdit()
        self.author_input.setMinimumHeight(35)
        if self.book:
            self.author_input.setText(self.book['author'])
        layout.addWidget(self.author_input)
        
        isbn_label = QLabel('ISBN:')
        isbn_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(isbn_label)
        self.isbn_input = QLineEdit()
        self.isbn_input.setMinimumHeight(35)
        if self.book:
            self.isbn_input.setText(self.book['isbn'] or '')
        layout.addWidget(self.isbn_input)
        
        category_label = QLabel('الفئة:')
        category_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(category_label)
        self.category_input = QLineEdit()
        self.category_input.setMinimumHeight(35)
        if self.book:
            self.category_input.setText(self.book['category'] or '')
        layout.addWidget(self.category_input)
        
        copies_label = QLabel('عدد النسخ:')
        copies_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(copies_label)
        self.copies_input = QSpinBox()
        self.copies_input.setMinimum(1)
        self.copies_input.setMinimumHeight(35)
        if self.book:
            self.copies_input.setValue(self.book['total_copies'])
        else:
            self.copies_input.setValue(1)
        layout.addWidget(self.copies_input)
        
        layout.addSpacing(10)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        save_btn = QPushButton('💾 حفظ')
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(120)
        cancel_btn = QPushButton('❌ إلغاء')
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def get_data(self):
        return {
            'title': self.title_input.text(),
            'author': self.author_input.text(),
            'isbn': self.isbn_input.text(),
            'category': self.category_input.text(),
            'total_copies': self.copies_input.value()
        }


class UserDialog(QDialog):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('معلومات المستخدم' if self.user else 'إضافة مستخدم جديد')
        self.setGeometry(100, 100, 450, 400)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        name_label = QLabel('الاسم:')
        name_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setMinimumHeight(35)
        if self.user:
            self.name_input.setText(self.user['name'])
        layout.addWidget(self.name_input)
        
        email_label = QLabel('البريد الإلكتروني:')
        email_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setMinimumHeight(35)
        if self.user:
            self.email_input.setText(self.user['email'] or '')
        layout.addWidget(self.email_input)
        
        phone_label = QLabel('الهاتف:')
        phone_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setMinimumHeight(35)
        if self.user:
            self.phone_input.setText(self.user['phone'] or '')
        layout.addWidget(self.phone_input)
        
        address_label = QLabel('العنوان:')
        address_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(address_label)
        self.address_input = QTextEdit()
        self.address_input.setMinimumHeight(80)
        if self.user:
            self.address_input.setText(self.user['address'] or '')
        layout.addWidget(self.address_input)
        
        layout.addSpacing(10)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        save_btn = QPushButton('💾 حفظ')
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(120)
        cancel_btn = QPushButton('❌ إلغاء')
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'address': self.address_input.toPlainText()
        }


class LoanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('إنشاء إعارة جديدة')
        self.setGeometry(100, 100, 450, 280)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        user_label = QLabel('المستخدم:')
        user_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(user_label)
        self.user_combo = QComboBox()
        self.user_combo.setMinimumHeight(35)
        self.load_users()
        layout.addWidget(self.user_combo)
        
        book_label = QLabel('الكتاب:')
        book_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(book_label)
        self.book_combo = QComboBox()
        self.book_combo.setMinimumHeight(35)
        self.load_books()
        layout.addWidget(self.book_combo)
        
        days_label = QLabel('مدة الإعارة (بالأيام):')
        days_label.setFont(QFont('Arial', 10, QFont.Bold))
        layout.addWidget(days_label)
        self.days_input = QSpinBox()
        self.days_input.setMinimum(1)
        self.days_input.setValue(14)
        self.days_input.setMinimumHeight(35)
        layout.addWidget(self.days_input)
        
        layout.addSpacing(10)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        create_btn = QPushButton('✅ إنشاء الإعارة')
        create_btn.setMinimumHeight(40)
        create_btn.setMinimumWidth(140)
        cancel_btn = QPushButton('❌ إلغاء')
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setMinimumWidth(120)
        create_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def load_users(self):
        users = UserModel.get_all_users()
        for user in users:
            self.user_combo.addItem(user['name'], user['id'])

    def load_books(self):
        books = BookModel.get_all_books()
        for book in books:
            if book['available_copies'] > 0:
                self.book_combo.addItem(f"{book['title']} - {book['author']}", book['id'])

    def get_data(self):
        return {
            'user_id': self.user_combo.currentData(),
            'book_id': self.book_combo.currentData(),
            'days': self.days_input.value()
        }


class BooksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        search_label = QLabel('🔍 البحث عن كتاب:')
        search_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('ابحث بالعنوان أو المؤلف أو ISBN...')
        self.search_input.setMinimumHeight(35)
        self.search_input.textChanged.connect(self.search_books)
        layout.addWidget(self.search_input)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'العنوان', 'المؤلف', 'ISBN', 'الفئة', 'العدد الكلي', 'المتاح'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setRowHeight(25, 30)
        self.table.setSelectionBehavior(1)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        add_btn = QPushButton('➕ إضافة كتاب')
        add_btn.setMinimumHeight(40)
        add_btn.setMinimumWidth(120)
        add_btn.clicked.connect(self.add_book)
        
        edit_btn = QPushButton('✏️ تعديل')
        edit_btn.setMinimumHeight(40)
        edit_btn.setMinimumWidth(100)
        edit_btn.clicked.connect(self.edit_book)
        
        delete_btn = QPushButton('🗑️ حذف')
        delete_btn.setMinimumHeight(40)
        delete_btn.setMinimumWidth(100)
        delete_btn.setObjectName('deleteBtn')
        delete_btn.clicked.connect(self.delete_book)
        
        refresh_btn = QPushButton('🔄 تحديث')
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_books)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.load_books()

    def load_books(self):
        books = BookModel.get_all_books()
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(book['title']))
            self.table.setItem(row, 2, QTableWidgetItem(book['author']))
            self.table.setItem(row, 3, QTableWidgetItem(book['isbn'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(book['category'] or ''))
            self.table.setItem(row, 5, QTableWidgetItem(str(book['total_copies'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(book['available_copies'])))

    def search_books(self):
        keyword = self.search_input.text()
        if keyword:
            books = BookModel.search_books(keyword)
        else:
            books = BookModel.get_all_books()
        
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(book['title']))
            self.table.setItem(row, 2, QTableWidgetItem(book['author']))
            self.table.setItem(row, 3, QTableWidgetItem(book['isbn'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(book['category'] or ''))
            self.table.setItem(row, 5, QTableWidgetItem(str(book['total_copies'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(book['available_copies'])))

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = BookModel.add_book(data['title'], data['author'], 
                                       data['isbn'], data['category'], 
                                       data['total_copies'])
            if result:
                QMessageBox.information(self, 'Success', 'Book added successfully')
                self.load_books()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to add book (ISBN may be duplicate)')

    def edit_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Error', 'Please select a book')
            return
        
        book_id = int(self.table.item(row, 0).text())
        book = BookModel.get_book_by_id(book_id)
        
        dialog = BookDialog(self, book)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if BookModel.update_book(book_id, data['title'], data['author'],
                                    data['isbn'], data['category'], 
                                    data['total_copies']):
                QMessageBox.information(self, 'Success', 'Book updated successfully')
                self.load_books()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to update book')

    def delete_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Error', 'Please select a book')
            return
        
        book_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, 'Confirm', 'Delete this book?',
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if BookModel.delete_book(book_id):
                QMessageBox.information(self, 'Success', 'Book deleted successfully')
                self.load_books()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to delete book')


class UsersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        search_label = QLabel('🔍 البحث عن مستخدم:')
        search_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('ابحث بالاسم أو البريد الإلكتروني...')
        self.search_input.setMinimumHeight(35)
        self.search_input.textChanged.connect(self.search_users)
        layout.addWidget(self.search_input)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'الاسم', 'البريد الإلكتروني', 'الهاتف', 'العنوان'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setRowHeight(25, 30)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        add_btn = QPushButton('➕ إضافة مستخدم')
        add_btn.setMinimumHeight(40)
        add_btn.setMinimumWidth(130)
        add_btn.clicked.connect(self.add_user)
        
        edit_btn = QPushButton('✏️ تعديل')
        edit_btn.setMinimumHeight(40)
        edit_btn.setMinimumWidth(100)
        edit_btn.clicked.connect(self.edit_user)
        
        delete_btn = QPushButton('🗑️ حذف')
        delete_btn.setMinimumHeight(40)
        delete_btn.setMinimumWidth(100)
        delete_btn.setObjectName('deleteBtn')
        delete_btn.clicked.connect(self.delete_user)
        
        refresh_btn = QPushButton('🔄 تحديث')
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_users)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        users = UserModel.get_all_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(user['name']))
            self.table.setItem(row, 2, QTableWidgetItem(user['email'] or ''))
            self.table.setItem(row, 3, QTableWidgetItem(user['phone'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(user['address'] or ''))

    def search_users(self):
        keyword = self.search_input.text()
        if keyword:
            users = UserModel.search_users(keyword)
        else:
            users = UserModel.get_all_users()
        
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(user['name']))
            self.table.setItem(row, 2, QTableWidgetItem(user['email'] or ''))
            self.table.setItem(row, 3, QTableWidgetItem(user['phone'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(user['address'] or ''))

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = UserModel.add_user(data['name'], data['email'],
                                       data['phone'], data['address'])
            if result:
                QMessageBox.information(self, 'Success', 'User added successfully')
                self.load_users()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to add user')

    def edit_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Error', 'Please select a user')
            return
        
        user_id = int(self.table.item(row, 0).text())
        user = UserModel.get_user_by_id(user_id)
        
        dialog = UserDialog(self, user)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if UserModel.update_user(user_id, data['name'], data['email'],
                                    data['phone'], data['address']):
                QMessageBox.information(self, 'Success', 'User updated successfully')
                self.load_users()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to update user')

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Error', 'Please select a user')
            return
        
        user_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, 'Confirm', 'Delete this user?',
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if UserModel.delete_user(user_id):
                QMessageBox.information(self, 'Success', 'User deleted successfully')
                self.load_users()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to delete user')


class LoansTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        filter_label = QLabel('📋 الفلترة:')
        filter_label.setFont(QFont('Arial', 11, QFont.Bold))
        layout.addWidget(filter_label)
        
        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['جميع الإعارات', 'الإعارات النشطة فقط'])
        self.filter_combo.setMinimumHeight(35)
        self.filter_combo.setMaximumWidth(300)
        self.filter_combo.currentTextChanged.connect(self.load_loans)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'المستخدم', 'الكتاب', 'تاريخ الإعارة', 'تاريخ الاستحقاق', 'تاريخ الإرجاع', 'الحالة', 'User ID', 'Book ID'])
        self.table.setColumnHidden(7, True)
        self.table.setColumnHidden(8, True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setRowHeight(25, 30)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        new_loan_btn = QPushButton('📚 إعارة جديدة')
        new_loan_btn.setMinimumHeight(40)
        new_loan_btn.setMinimumWidth(130)
        new_loan_btn.clicked.connect(self.create_loan)
        
        return_btn = QPushButton('↩️ إرجاع كتاب')
        return_btn.setMinimumHeight(40)
        return_btn.setMinimumWidth(120)
        return_btn.clicked.connect(self.return_book)
        
        refresh_btn = QPushButton('🔄 تحديث')
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setMinimumWidth(100)
        refresh_btn.clicked.connect(self.load_loans)
        
        btn_layout.addWidget(new_loan_btn)
        btn_layout.addWidget(return_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.load_loans()

    def load_loans(self):
        if self.filter_combo.currentText() == 'الإعارات النشطة فقط':
            loans = LoanModel.get_active_loans()
        else:
            loans = LoanModel.get_all_loans()
        
        self.table.setRowCount(len(loans))
        for row, loan in enumerate(loans):
            self.table.setItem(row, 0, QTableWidgetItem(str(loan['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(loan['name']))
            self.table.setItem(row, 2, QTableWidgetItem(loan['title']))
            self.table.setItem(row, 3, QTableWidgetItem(loan['loan_date'][:10] if loan['loan_date'] else ''))
            self.table.setItem(row, 4, QTableWidgetItem(loan['due_date'][:10] if loan['due_date'] else ''))
            self.table.setItem(row, 5, QTableWidgetItem(loan['return_date'][:10] if loan['return_date'] else ''))
            self.table.setItem(row, 6, QTableWidgetItem(loan['status']))
            self.table.setItem(row, 7, QTableWidgetItem(str(loan['user_id'])))
            self.table.setItem(row, 8, QTableWidgetItem(str(loan['book_id'])))

    def create_loan(self):
        dialog = LoanDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = LoanModel.create_loan(data['user_id'], data['book_id'], data['days'])
            if result:
                QMessageBox.information(self, 'Success', 'Loan created successfully')
                self.load_loans()
            else:
                QMessageBox.warning(self, 'Error', 'Failed to create loan')

    def return_book(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Error', 'Please select a loan')
            return
        
        loan_id = int(self.table.item(row, 0).text())
        status = self.table.item(row, 6).text()
        
        if status != 'active':
            QMessageBox.warning(self, 'Error', 'Only active loans can be returned')
            return
        
        if LoanModel.return_book(loan_id):
            QMessageBox.information(self, 'Success', 'Book returned successfully')
            self.load_loans()
        else:
            QMessageBox.warning(self, 'Error', 'Failed to return book')


class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel('📊 التقرير: أكثر الكتب استعارة')
        title_label.setFont(QFont('Arial', 13, QFont.Bold))
        layout.addWidget(title_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'العنوان', 'المؤلف', 'عدد الإعارات'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setRowHeight(25, 30)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton('🔄 تحديث التقرير')
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setMinimumWidth(130)
        refresh_btn.clicked.connect(self.load_report)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.load_report()

    def load_report(self):
        books = LoanModel.get_most_borrowed_books()
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(book['title']))
            self.table.setItem(row, 2, QTableWidgetItem(book['author']))
            self.table.setItem(row, 3, QTableWidgetItem(str(book['borrow_count'])))


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        init_database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('📚 نظام إدارة المكتبة الحديث')
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(1000, 600)
        
        tabs = QTabWidget()
        tabs.addTab(BooksTab(), '📖 الكتب')
        tabs.addTab(UsersTab(), '👥 المستخدمون')
        tabs.addTab(LoansTab(), '📚 الإعارات')
        tabs.addTab(ReportsTab(), '📊 التقارير')
        
        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    app.setStyleSheet(STYLESHEET)
    
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
