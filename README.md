# 📚 Library Management System

A modern, professional desktop application for managing books, users, and loan records. Built with Python, PyQt5, and SQLite3.

## 🌟 Features

### 📖 Books Management
- ✅ Add new books with detailed information
- ✅ Edit existing book records
- ✅ Delete books from the system
- ✅ Real-time search functionality (title, author, ISBN)
- ✅ Track available and total copies
- ✅ Categorize books
- ✅ ISBN unique constraint

### 👥 User Management
- ✅ Register new library members
- ✅ Update user information
- ✅ Delete user accounts
- ✅ Real-time search (name, email)
- ✅ Store contact details and address
- ✅ Track membership dates
- ✅ Email uniqueness validation

### 📚 Loan Management
- ✅ Create new book loans
- ✅ Track loan duration (default 14 days)
- ✅ Record book returns
- ✅ Filter active loans
- ✅ View loan history
- ✅ Display due dates and return dates
- ✅ Automatic book availability updates

### 📊 Reports & Analytics
- ✅ Most borrowed books report
- ✅ Borrowing statistics
- ✅ Track book popularity
- ✅ Refresh reports in real-time

### 🎨 User Interface
- ✅ Professional dark blue theme
- ✅ Intuitive tabbed interface
- ✅ Full Arabic and English support
- ✅ Emoji-enhanced buttons for quick identification
- ✅ Responsive dialog windows
- ✅ Real-time search with live results
- ✅ Clean and organized tables
- ✅ Error handling with user feedback

## 📋 Requirements

- **Python**: 3.7 or higher
- **PyQt5**: 5.15 or higher
- **SQLite3**: Included with Python
- **Operating System**: Windows, macOS, or Linux

## 🔧 Installation

### 1. Ensure Python is installed
```bash
python --version
```

### 2. Install PyQt5
```bash
pip install PyQt5
```

### 3. Clone or download the project
```bash
cd path/to/project
```

## 🚀 Running the Application

```bash
python main.py
```

The application will automatically create the SQLite database on first run.

## 📁 Project Structure

```
Library Management System/
│
├── main.py                 # Main application window and GUI
├── database.py             # Database initialization and connection management
├── models.py               # Data models and business logic
├── library.db              # SQLite3 database (auto-created)
├── README.md              # This file
├── README.txt             # Quick reference guide
└── __pycache__/           # Python cache directory
```

## 🏗️ Architecture

### Three-Tier Architecture

#### 1. **Presentation Layer** (`main.py`)
- PyQt5 GUI components
- User interface windows and dialogs
- Event handling and user interactions
- Real-time search and filtering
- Four main tabs: Books, Users, Loans, Reports

#### 2. **Business Logic Layer** (`models.py`)
- `BookModel`: CRUD operations for books
- `UserModel`: CRUD operations for users
- `LoanModel`: Loan management and statistics
- Search and filtering functions
- Data validation

#### 3. **Data Layer** (`database.py`)
- SQLite3 database connection
- Database initialization
- Table schema creation
- Helper functions for data serialization

## 💾 Database Schema

### Books Table
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    category TEXT,
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Fields:**
- `id`: Unique book identifier
- `title`: Book title (required)
- `author`: Author name (required)
- `isbn`: ISBN number (unique)
- `category`: Book category/genre
- `total_copies`: Total number of book copies
- `available_copies`: Currently available copies
- `created_at`: Creation timestamp

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Fields:**
- `id`: Unique user identifier
- `name`: Full name (required)
- `email`: Email address (unique)
- `phone`: Phone number
- `address`: Physical address
- `membership_date`: Account creation date

### Loans Table
```sql
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    return_date TIMESTAMP,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
)
```

**Fields:**
- `id`: Unique loan identifier
- `user_id`: Reference to user (Foreign Key)
- `book_id`: Reference to book (Foreign Key)
- `loan_date`: When the book was borrowed
- `due_date`: When the book is due
- `return_date`: When the book was returned (NULL if not returned)
- `status`: 'active' or 'returned'

## 📚 Module Documentation

### main.py

#### Classes

##### `BookDialog(QDialog)`
Dialog window for adding/editing books.
- **Methods:**
  - `init_ui()`: Initialize dialog UI
  - `get_data()`: Return book data from form

##### `UserDialog(QDialog)`
Dialog window for adding/editing users.
- **Methods:**
  - `init_ui()`: Initialize dialog UI
  - `get_data()`: Return user data from form

##### `LoanDialog(QDialog)`
Dialog window for creating new loans.
- **Methods:**
  - `init_ui()`: Initialize dialog UI
  - `load_users()`: Populate user dropdown
  - `load_books()`: Populate available books dropdown
  - `get_data()`: Return loan data from form

##### `BooksTab(QWidget)`
Tab for managing books.
- **Methods:**
  - `init_ui()`: Initialize tab UI
  - `load_books()`: Load all books into table
  - `search_books()`: Search books in real-time
  - `add_book()`: Create new book
  - `edit_book()`: Modify existing book
  - `delete_book()`: Remove book

##### `UsersTab(QWidget)`
Tab for managing users.
- **Methods:**
  - `init_ui()`: Initialize tab UI
  - `load_users()`: Load all users into table
  - `search_users()`: Search users in real-time
  - `add_user()`: Register new user
  - `edit_user()`: Modify user information
  - `delete_user()`: Remove user account

##### `LoansTab(QWidget)`
Tab for managing book loans.
- **Methods:**
  - `init_ui()`: Initialize tab UI
  - `load_loans()`: Load loans based on filter
  - `create_loan()`: Create new loan
  - `return_book()`: Record book return

##### `ReportsTab(QWidget)`
Tab for viewing reports and statistics.
- **Methods:**
  - `init_ui()`: Initialize tab UI
  - `load_report()`: Load most borrowed books

##### `LibraryApp(QMainWindow)`
Main application window.
- **Methods:**
  - `init_ui()`: Initialize main window
  - `main()`: Application entry point

### database.py

#### Functions

##### `init_database()`
Initializes the SQLite database with all required tables.
- Creates `books` table
- Creates `users` table
- Creates `loans` table
- Returns: None

##### `get_connection()`
Establishes a connection to the SQLite database.
- Returns: `sqlite3.Connection` object
- Usage: Always close connection after use

##### `dict_factory(cursor, row)`
Converts database row tuple to dictionary.
- Parameters:
  - `cursor`: Database cursor with column descriptions
  - `row`: Row data tuple
- Returns: Dictionary with column names as keys

### models.py

#### BookModel (Static Methods)

##### `add_book(title, author, isbn, category, total_copies)`
Adds a new book to the database.
- Parameters: Book details
- Returns: Book ID or None if error

##### `update_book(book_id, title, author, isbn, category, total_copies)`
Updates existing book information.
- Parameters: Book ID and updated details
- Returns: True if successful, False otherwise

##### `delete_book(book_id)`
Removes a book from the database.
- Parameters: Book ID
- Returns: True if successful, False otherwise

##### `get_all_books()`
Retrieves all books from database.
- Returns: List of book dictionaries

##### `get_book_by_id(book_id)`
Retrieves a specific book.
- Parameters: Book ID
- Returns: Book dictionary or None

##### `search_books(keyword)`
Searches books by title, author, or ISBN.
- Parameters: Search keyword
- Returns: List of matching books

#### UserModel (Static Methods)

##### `add_user(name, email, phone, address)`
Registers a new library user.
- Parameters: User details
- Returns: User ID or None if error

##### `update_user(user_id, name, email, phone, address)`
Updates user information.
- Parameters: User ID and updated details
- Returns: True if successful, False otherwise

##### `delete_user(user_id)`
Removes a user from the database.
- Parameters: User ID
- Returns: True if successful, False otherwise

##### `get_all_users()`
Retrieves all users from database.
- Returns: List of user dictionaries

##### `get_user_by_id(user_id)`
Retrieves a specific user.
- Parameters: User ID
- Returns: User dictionary or None

##### `search_users(keyword)`
Searches users by name or email.
- Parameters: Search keyword
- Returns: List of matching users

#### LoanModel (Static Methods)

##### `create_loan(user_id, book_id, days=14)`
Creates a new book loan and updates availability.
- Parameters:
  - `user_id`: User borrowing the book
  - `book_id`: Book being borrowed
  - `days`: Loan duration (default 14)
- Returns: Loan ID or None if error
- Side Effects: Decrements `available_copies`

##### `return_book(loan_id)`
Records book return and updates availability.
- Parameters: Loan ID
- Returns: True if successful, False otherwise
- Side Effects: Increments `available_copies`, sets status to 'returned'

##### `get_all_loans()`
Retrieves all loan records with user and book details.
- Returns: List of loan dictionaries with joined data

##### `get_active_loans()`
Retrieves only active (unreturned) loans.
- Returns: List of active loan dictionaries

##### `get_most_borrowed_books(limit=10)`
Generates report of most borrowed books.
- Parameters: Number of books to return (default 10)
- Returns: List of books with borrow counts

## 🎯 Usage Guide

### Adding a Book
1. Click on the "📖 Books" tab
2. Click "➕ Add Book" button
3. Fill in book details (Title, Author, ISBN, Category, Copies)
4. Click "💾 Save"

### Adding a User
1. Click on "👥 Users" tab
2. Click "➕ Add User" button
3. Fill in user information (Name, Email, Phone, Address)
4. Click "💾 Save"

### Creating a Loan
1. Click on "📚 Loans" tab
2. Click "📚 New Loan" button
3. Select user and book from dropdowns
4. Set loan duration (default 14 days)
5. Click "✅ Create Loan"

### Returning a Book
1. Click on "📚 Loans" tab
2. Select the loan from the active loans list
3. Click "↩️ Return Book"
4. Confirm the return

### Searching for Books
1. Go to "📖 Books" tab
2. Type in the search box (searches by title, author, or ISBN)
3. Results update in real-time

### Viewing Reports
1. Click on "📊 Reports" tab
2. View the most borrowed books statistics
3. Click "🔄 Update Report" to refresh

## 🛠️ Development

### Adding New Features

1. **New Database Fields**
   - Modify schema in `database.py`
   - Update model methods in `models.py`
   - Add UI elements in `main.py`

2. **New Functionality**
   - Add methods to appropriate model class
   - Create corresponding dialog if needed
   - Add button and handler in tab class

3. **Database Queries**
   - Use parameterized queries to prevent SQL injection
   - Always close database connections
   - Handle exceptions gracefully

### Testing
```bash
python -m py_compile main.py models.py database.py
```

## ⚙️ Configuration

### Default Loan Duration
Located in `LoanDialog.__init__()`:
```python
self.days_input.setValue(14)  # Change to desired days
```

### Database Location
Located in `database.py`:
```python
DB_PATH = Path(__file__).parent / 'library.db'
```

### Styling
Located in `main.py` as `STYLESHEET` variable. Modify CSS properties to change colors and appearance.

## 🐛 Troubleshooting

### Application Won't Start
- Ensure PyQt5 is installed: `pip install PyQt5`
- Check Python version: `python --version`
- Verify all files are in the same directory

### Database Issues
- Delete `library.db` file to reset database
- Check file permissions in project directory
- Ensure SQLite3 is available on your system

### Import Errors
```bash
pip install --upgrade PyQt5
python -m pip install --force-reinstall PyQt5
```

### GUI Issues
- Update graphics drivers if available
- Try running with Python 3.9 or higher
- Check system display settings

## 📄 File Information

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| main.py | 29 KB | 823 | GUI and user interface |
| database.py | 1.8 KB | 66 | Database management |
| models.py | 8.8 KB | 294 | Business logic |
| library.db | 28 KB | N/A | SQLite database |

## 🔒 Security Features

- ✅ Parameterized SQL queries (prevents SQL injection)
- ✅ Input validation on forms
- ✅ Foreign key constraints
- ✅ Unique constraints (ISBN, Email)
- ✅ Exception handling for database errors
- ✅ Read-only query operations where appropriate

## 📝 License

This project is open source and available for educational and personal use.

## 👨‍💻 Author

Developed as a modern library management system demonstrating:
- PyQt5 GUI development
- SQLite3 database management
- Model-View-Controller architecture
- Real-time search functionality
- Professional UI/UX design

## 🚀 Future Enhancements

- [ ] User authentication and login system
- [ ] PDF report export functionality
- [ ] Email notifications for due dates
- [ ] Fine calculation for overdue books
- [ ] Book cover image storage
- [ ] Advanced analytics and charts
- [ ] Multi-user access with permissions
- [ ] Backup and restore functionality
- [ ] Dark mode theme toggle
- [ ] Database migration tools

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all files are present
3. Ensure PyQt5 is properly installed
4. Check Python version compatibility

## 📚 Additional Resources

- [PyQt5 Documentation](https://doc.qt.io/qt-5/)
- [SQLite3 Documentation](https://www.sqlite.org/docs.html)
- [Python Official Documentation](https://docs.python.org/3/)

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Status**: Stable and Production Ready ✅
