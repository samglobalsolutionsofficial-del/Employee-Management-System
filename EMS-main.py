import sqlite3

class Employee:
    def __init__(self, id, full_name, email, phone, date_of_birth, bank_account):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.bank_account = bank_account

    # Alternative constructor 1: from a DB row tuple
    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4], row[5])

    # Alternative constructor 2: from form input strings
    @classmethod
    def from_form(cls, full_name, email, phone, dob_str, bank_account):
        if not full_name.strip():
            raise ValueError("Full name cannot be empty")
        if not email.strip():
            raise ValueError("Email cannot be empty")
        if not phone.strip():
            raise ValueError("Phone cannot be empty")
        if not dob_str.strip():
            raise ValueError("Date of birth cannot be empty")
        if not bank_account.strip():
            raise ValueError("Bank account cannot be empty")
        return cls(None, full_name.strip(), email.strip(), phone.strip(), dob_str.strip(), bank_account.strip())

    def __str__(self):
        return f"[{self.id}] {self.full_name}, {self.email}, {self.phone}"

# DB setup
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    bank_account TEXT NOT NULL
)
""")
conn.commit()

def save_employee(emp):
    cursor.execute(
        "INSERT INTO employees (full_name, email, phone, date_of_birth, bank_account) VALUES (?,?,?,?,?)",
        (emp.full_name, emp.email, emp.phone, emp.date_of_birth, emp.bank_account)
    )
    conn.commit()
    emp.id = cursor.lastrowid
    return emp

def get_all_employees():
    cursor.execute("SELECT id, full_name, email, phone, date_of_birth, bank_account FROM employees")
    rows = cursor.fetchall()
    return [Employee.from_db_row(row) for row in rows]

def delete_employee(emp_id):
    cursor.execute("DELETE FROM employees WHERE id =?", (emp_id,))
    conn.commit()
    return cursor.rowcount > 0

def update_employee(emp_id, full_name, email, phone, date_of_birth, bank_account):
    cursor.execute(
        "UPDATE employees SET full_name=?, email=?, phone=?, date_of_birth=?, bank_account=? WHERE id=?",
        (full_name, email, phone, date_of_birth, bank_account, emp_id)
    )
    conn.commit()
    return cursor.rowcount > 0

def print_table(data, headers):
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    top = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    mid = "+" + "+".join("=" * (w + 2) for w in col_widths) + "+"
    bottom = top

    print(top)
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |")
    print(mid)
    for row in data:
        print("| " + " | ".join(str(v).ljust(w) for v, w in zip(row, col_widths)) + " |")
    print(bottom)

def main():
    def show_menu():
        title = "EMPLOYEE MANAGEMENT MENU COMMMANDS"
        options = [
            ("Add", "Add employee"),
            ("Show", "Show all employees"),
            ("Delete", "Delete employee"),
            ("Update", "Update employee"),
            ("Exit", "Exit the program")
        ]

        width = 50
        border = "═" * width

        print("\n╔" + border + "╗")
        print("║" + title.center(width) + "║")
        print("╠" + border + "╣")

        for cmd, desc in options:
            line = f" {cmd:<6} ➜ {desc}"
            print("║" + line.ljust(width) + "║")

        print("╚" + border + "╝")
    show_menu()

    while True:
        CYAN = "\033[96m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

        choice = input(f"\n{CYAN}{BOLD}❯{RESET} Enter command {CYAN}»{RESET} ").lower().strip()

        if choice == "":
            print("⚠️ You didn't type anything. Use the menu above.")

        elif choice == "add":
            CYAN = "\033[96m"
            GREEN = "\033[92m"
            RED = "\033[91m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            print(f"\n{CYAN}{BOLD}➕ Add New Employee{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            full_name = input(f" {BOLD}Full Name: {RESET}").strip()
            email = input(f" {BOLD}Email: {RESET}").strip()
            phone = input(f" {BOLD}Phone: {RESET}").strip()
            dob = input(f" {BOLD}Date of Birth YYYY-MM-DD: {RESET}").strip()
            bank_account = input(f" {BOLD}Bank Account No: {RESET}").strip()
            try:
                emp = Employee.from_form(full_name, email, phone, dob, bank_account)
                save_employee(emp)
                headers = ["ID", "Full Name", "Email", "Phone", "DOB", "Bank Account"]
                row = [emp.id, emp.full_name, emp.email, emp.phone, emp.date_of_birth, emp.bank_account]
                print(f"\n{GREEN}✅ Employee saved successfully!{RESET}")
                print_table([row], headers)
            except ValueError as e:
                print(f"\n{RED}❌ Error: {e}{RESET}")

        elif choice == "show":
            CYAN = "\033[96m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            employees = get_all_employees()
            print(f"\n{CYAN}{BOLD}📋 Show All Employees{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            if not employees:
                print("ℹ️ No employees found")
            else:
                headers = ["ID", "Full Name", "Email", "Phone", "DOB", "Bank Account"]
                data = [[e.id, e.full_name, e.email, e.phone, e.date_of_birth, e.bank_account] for e in employees]
                print_table(data, headers)

        elif choice == "delete":
            CYAN = "\033[96m"
            RED = "\033[91m"
            GREEN = "\033[92m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            print(f"\n{CYAN}{BOLD}🗑️ Delete Employee{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            try:
                emp_id = int(input(f" {BOLD}Enter Employee ID to delete: {RESET}").strip())
                cursor.execute("SELECT * FROM employees WHERE id =?", (emp_id,))
                row = cursor.fetchone()
                if row:
                    print(f"\n{RED}⚠️ About to delete this employee:{RESET}")
                    print_table([row], ["ID", "Full Name", "Email", "Phone", "DOB", "Bank Account"])
                    cursor.execute("DELETE FROM employees WHERE id =?", (emp_id,))
                    conn.commit()
                    print(f"\n{GREEN}✅ Employee {emp_id} deleted successfully!{RESET}")
                else:
                    print(f"\n{RED}❌ No employee found with ID {emp_id}{RESET}")
            except ValueError:
                print(f"\n{RED}❌ Invalid ID. Enter a number.{RESET}")

        elif choice == "update":
            CYAN = "\033[96m"
            YELLOW = "\033[93m"
            GREEN = "\033[92m"
            RED = "\033[91m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            print(f"\n{CYAN}{BOLD}✏️ Update Employee{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            try:
                emp_id = int(input(f" {BOLD}Enter Employee ID to update: {RESET}").strip())
                cursor.execute("SELECT * FROM employees WHERE id =?", (emp_id,))
                old_row = cursor.fetchone()
                if not old_row:
                    print(f"\n{RED}❌ No employee found with ID {emp_id}{RESET}")
                else:
                    headers = ["ID", "Full Name", "Email", "Phone", "DOB", "Bank Account"]
                    print(f"\n{YELLOW}Old Data:{RESET}")
                    print_table([old_row], headers)

                    print(f"\n{BOLD}Enter new values. Press Enter to keep current value:{RESET}")
                    new_name = input(f" Full Name [{old_row[1]}]: ").strip() or old_row[1]
                    new_email = input(f" Email [{old_row[2]}]: ").strip() or old_row[2]
                    new_phone = input(f" Phone [{old_row[3]}]: ").strip() or old_row[3]
                    new_dob = input(f" DOB [{old_row[4]}]: ").strip() or old_row[4]
                    new_bank = input(f" Bank Account [{old_row[5]}]: ").strip() or old_row[5]

                    if update_employee(emp_id, new_name, new_email, new_phone, new_dob, new_bank):
                        cursor.execute("SELECT * FROM employees WHERE id =?", (emp_id,))
                        new_row = cursor.fetchone()
                        print(f"\n{GREEN}✅ Employee updated successfully!{RESET}")
                        print(f"\n{GREEN}New Data:{RESET}")
                        print_table([new_row], headers)
                    else:
                        print(f"\n{RED}❌ Update failed{RESET}")
            except ValueError:
                print(f"\n{RED}❌ Invalid ID. Enter a number.{RESET}")

        elif choice == 'exit':
            CYAN = "\033[96m"
            GREEN = "\033[92m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            msg = "Exiting the program. Goodbye!"
            width = len(msg) + 7
            print(f"\n{CYAN}╔{'═' * width}╗{RESET}")
            print(f"{CYAN}║{RESET} {GREEN}{BOLD}👋 {msg}{RESET} {CYAN}  ║{RESET}")
            print(f"{CYAN}╚{'═' * width}╝{RESET}")
            break
        else:
            print("❌ Invalid input. Try again.")

    conn.close()

if __name__ == '__main__':
    main()