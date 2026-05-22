<div align="center">

<br/>

```
███████╗███╗   ███╗██████╗ ██╗      ██████╗ ██╗   ██╗███████╗███████╗
██╔════╝████╗ ████║██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝██╔════╝██╔════╝
█████╗  ██╔████╔██║██████╔╝██║     ██║   ██║ ╚████╔╝ █████╗  █████╗  
██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██║   ██║  ╚██╔╝  ██╔══╝  ██╔══╝  
███████╗██║ ╚═╝ ██║██║     ███████╗╚██████╔╝   ██║   ███████╗███████╗
╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝
```

# 👥 Employee Management System

**A powerful, terminal-based CRUD application built with Python & SQLite3**

<br/>

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite3-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-8b5cf6?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge)

<br/>

</div>

---

## 📖 Overview

A clean, interactive **command-line Employee Management System** that lets you store, retrieve, update, and delete employee records with zero external dependencies. All data is persisted in a local **SQLite3 database** (`employees.db`), meaning your records survive between sessions without any server setup.

> 💡 Perfect for learning Python OOP patterns, SQLite3 integration, and clean CLI design.

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ **Add Employee** | Register a new employee with full validation |
| 📋 **Show All** | View every employee in a formatted ASCII table |
| ✏️ **Update Employee** | Edit any field; press Enter to keep existing value |
| 🗑️ **Delete Employee** | Remove a record by ID with a confirmation preview |
| 🎨 **Coloured UI** | ANSI colour codes for a polished terminal experience |
| 🛡️ **Input Validation** | Guards against empty fields and invalid data types |
| 💾 **Persistent Storage** | SQLite3 file-based database — no server required |

---

## 🗂️ Project Structure

```
employee-management/
│
├── 📄 EMS-main.py              ← Entry point — all logic lives here
├── 🗃️ employees.db             ← Auto-created on first run (SQLite3)
└── 📘 README.md                ← You are here
```

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────┐
│  Language   →  Python 3.8+              │
│  Database   →  SQLite3 (built-in)       │
│  UI Layer   →  Terminal / ANSI colours  │
│  ORM        →  None (raw SQL + cursor)  │
│  Packaging  →  No external deps needed  │
└─────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or higher** installed
- No `pip install` needed — uses the Python standard library only

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/employee-management.git

# 2. Navigate into the project folder
cd employee-management

# 3. Run the application
python main.py
```

The `employees.db` file is created automatically on the first run.

---

## 💻 Usage

Once running, you'll see the interactive menu:

```
╔══════════════════════════════════════════════════╗
║     EMPLOYEE MANAGEMENT MENU COMMMANDS           ║
╠══════════════════════════════════════════════════╣
║  Add    ➜ Add employee                          ║
║  Show   ➜ Show all employees                    ║
║  Delete ➜ Delete employee                       ║
║  Update ➜ Update employee                       ║
║  Exit   ➜ Exit the program                      ║
╚══════════════════════════════════════════════════╝
```

Type any command and press **Enter**:

```
❯ Enter command » add
```

### Command Reference

```
add     →  Prompt for employee details and save to DB
show    →  Print all employee records as a table
delete  →  Delete a record by numeric ID
update  →  Edit a record field-by-field (keep blank to retain)
exit    →  Gracefully close the DB connection and quit
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE IF NOT EXISTS employees (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT     NOT NULL,
    email         TEXT     NOT NULL UNIQUE,
    phone         TEXT     NOT NULL,
    date_of_birth TEXT     NOT NULL,
    bank_account  TEXT     NOT NULL
);
```

> ⚠️ `email` has a `UNIQUE` constraint — duplicate emails are rejected at the database level.

---

## 🏗️ Architecture

The project follows an **OOP + functional hybrid** design:

```
Employee (class)
├── __init__()          ← Standard constructor
├── from_db_row()       ← Classmethod: build from SQLite tuple
├── from_form()         ← Classmethod: build from user input + validate
└── __str__()           ← Human-readable representation

Database helpers (module-level functions)
├── save_employee()     ← INSERT and return auto-generated ID
├── get_all_employees() ← SELECT all → list[Employee]
├── delete_employee()   ← DELETE by ID
└── update_employee()   ← UPDATE all fields by ID

UI helpers
├── print_table()       ← Dynamic-width ASCII table renderer
└── main() / show_menu()← REPL loop with ANSI colour prompts
```

---

## 🛡️ Input Validation

All user input is validated inside `Employee.from_form()` before any database write:

- ❌ Empty `full_name`, `email`, `phone`, `date_of_birth`, or `bank_account` raises `ValueError`
- ❌ Non-integer Employee ID for `delete` / `update` raises `ValueError` (caught in the REPL)
- ✅ All values are `.strip()`-ed to remove accidental whitespace

---

## 📸 Sample Output

```
➕ Add New Employee
─────────────────────
 Full Name: Jane Doe
 Email: jane@example.com
 Phone: +92-333-1234567
 Date of Birth YYYY-MM-DD: 1995-06-15
 Bank Account No: PK36SCBL0000001123456702

✅ Employee saved successfully!
+----+-----------+------------------+------------------+------------+---------------------------+
| ID | Full Name | Email            | Phone            | DOB        | Bank Account              |
+====+===========+==================+==================+============+===========================+
| 1  | Jane Doe  | jane@example.com | +92-333-1234567  | 1995-06-15 | PK36SCBL0000001123456702  |
+----+-----------+------------------+------------------+------------+---------------------------+
```

---

## 🔮 Possible Improvements

- [ ] Add **email format validation** with regex
- [ ] Add **date-of-birth format validation** (enforce `YYYY-MM-DD`)
- [ ] Add **search / filter** by name or email
- [ ] Export records to **CSV**
- [ ] Encrypt `bank_account` at rest
- [ ] Add a **pagination** view for large datasets
- [ ] Migrate CLI to a **Rich** or **Textual** TUI for richer visuals

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork → clone → create branch
git checkout -b feature/your-feature-name

# Make changes, then commit
git commit -m "feat: add your feature description"

# Push and open a Pull Request
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

Made with ❤️ and Python

**[⭐ Star this repo if you found it useful!]**

</div>
