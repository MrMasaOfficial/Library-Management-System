import sqlite3
from database import get_connection, dict_factory
from datetime import datetime, timedelta


class BookModel:
    @staticmethod
    def add_book(title, author, isbn, category, total_copies):
        """Add a new book to database."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO books (title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, category, total_copies, total_copies))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def update_book(book_id, title, author, isbn, category, total_copies):
        """Update book information."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE books
                SET title = ?, author = ?, isbn = ?, category = ?, total_copies = ?
                WHERE id = ?
            ''', (title, author, isbn, category, total_copies, book_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_book(book_id):
        """Delete a book."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_books():
        """Get all books."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books ORDER BY title')
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def get_book_by_id(book_id):
        """Get book by ID."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        conn.close()
        return book

    @staticmethod
    def search_books(keyword):
        """Search books by title, author, or ISBN."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        search_term = f'%{keyword}%'
        cursor.execute('''
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
            ORDER BY title
        ''', (search_term, search_term, search_term))
        books = cursor.fetchall()
        conn.close()
        return books


class UserModel:
    @staticmethod
    def add_user(name, email, phone, address):
        """Add a new user."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone, address))
            conn.commit()
            return cursor.lastrowid
        except Exception:
            return None
        finally:
            conn.close()

    @staticmethod
    def update_user(user_id, name, email, phone, address):
        """Update user information."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE users
                SET name = ?, email = ?, phone = ?, address = ?
                WHERE id = ?
            ''', (name, email, phone, address, user_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_user(user_id):
        """Delete a user."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_users():
        """Get all users."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY name')
        users = cursor.fetchall()
        conn.close()
        return users

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def search_users(keyword):
        """Search users by name or email."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        search_term = f'%{keyword}%'
        cursor.execute('''
            SELECT * FROM users
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY name
        ''', (search_term, search_term))
        users = cursor.fetchall()
        conn.close()
        return users


class LoanModel:
    @staticmethod
    def create_loan(user_id, book_id, days=14):
        """Create a new loan."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            due_date = datetime.now() + timedelta(days=days)
            cursor.execute('''
                INSERT INTO loans (user_id, book_id, due_date, status)
                VALUES (?, ?, ?, ?)
            ''', (user_id, book_id, due_date.isoformat(), 'active'))
            
            cursor.execute('''
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id = ?
            ''', (book_id,))
            
            conn.commit()
            return cursor.lastrowid
        except Exception:
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def return_book(loan_id):
        """Return a borrowed book."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT book_id FROM loans WHERE id = ?', (loan_id,))
            result = cursor.fetchone()
            if result:
                book_id = result[0]
                cursor.execute('''
                    UPDATE loans
                    SET return_date = ?, status = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), 'returned', loan_id))
                
                cursor.execute('''
                    UPDATE books
                    SET available_copies = available_copies + 1
                    WHERE id = ?
                ''', (book_id,))
                
                conn.commit()
                return True
        except Exception:
            conn.rollback()
        finally:
            conn.close()
        return False

    @staticmethod
    def get_all_loans():
        """Get all loans."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.id, l.user_id, l.book_id, u.name, b.title, 
                   l.loan_date, l.due_date, l.return_date, l.status
            FROM loans l
            JOIN users u ON l.user_id = u.id
            JOIN books b ON l.book_id = b.id
            ORDER BY l.loan_date DESC
        ''')
        loans = cursor.fetchall()
        conn.close()
        return loans

    @staticmethod
    def get_active_loans():
        """Get active loans only."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.id, l.user_id, l.book_id, u.name, b.title, 
                   l.loan_date, l.due_date, l.return_date, l.status
            FROM loans l
            JOIN users u ON l.user_id = u.id
            JOIN books b ON l.book_id = b.id
            WHERE l.status = 'active'
            ORDER BY l.due_date
        ''')
        loans = cursor.fetchall()
        conn.close()
        return loans

    @staticmethod
    def get_most_borrowed_books(limit=10):
        """Get most borrowed books."""
        conn = get_connection()
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.id, b.title, b.author, COUNT(l.id) as borrow_count
            FROM books b
            LEFT JOIN loans l ON b.id = l.book_id
            GROUP BY b.id
            ORDER BY borrow_count DESC
            LIMIT ?
        ''', (limit,))
        books = cursor.fetchall()
        conn.close()
        return books
