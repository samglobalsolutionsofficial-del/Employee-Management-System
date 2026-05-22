
import sqlite3

class User:
    def __init__(self, id, name, age, email):
        self.id = id
        self.name = name
        self.age = int(age)
        self.email = email

    # Alternative constructor 1: from a DB row tuple
    @classmethod
    def from_db_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])

    # Alternative constructor 2: from form input strings
    @classmethod
    def from_form(cls, name, age_str, email):
        try:
            age = int(age_str)
            if age < 0:
                raise ValueError("Age can't be negative")
            return cls(None, name, age, email) # id=None before saving
        except ValueError as e:
            raise ValueError(f"Invalid form data: {e}")

    def __str__(self):
        return f"[{self.id}] {self.name}, {self.age} yrs, {self.email}"

# DB setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")
conn.commit()

def save_user(user):
    cursor.execute(
        "INSERT INTO users (name, age, email) VALUES (?,?,?)",
        (user.name, user.age, user.email)
    )
    conn.commit()
    user.id = cursor.lastrowid
    return user

def get_all_users():
    cursor.execute("SELECT id, name, age, email FROM users")
    rows = cursor.fetchall()
    # Use alternative constructor to convert each row to User object
    return [User.from_db_row(row) for row in rows]

def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return cursor.rowcount > 0  # True if a row was deleted

def update_user(user_id, name, age, email):
    cursor.execute(
        "UPDATE users SET name =?, age =?, email =? WHERE id =?",
        (name, age, email, user_id)
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
        title = "USER MANAGEMENT MENU COMMANDSAD"
        options = [
            ("Add", "Add user "),
            ("Show", "Show all users"),
            ("Delete", "Delete user"),
            ("Update", "Update user"),
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
            print("⚠️  You didn't type anything. Use the menu above.")


        elif choice == "add":
            # ANSI color codes
            CYAN = "\033[96m"
            GREEN = "\033[92m"
            RED = "\033[91m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            print(f"\n{CYAN}{BOLD}➕ Add New User{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            name = input(f" {BOLD}Name :{RESET} ").strip()
            age = input(f" {BOLD}Age :{RESET} ").strip()
            email = input(f" {BOLD}Email:{RESET} ").strip()
            try:
                user = User.from_form(name, age, email)
                save_user(user)
                # Print saved user in table format
                headers = ["ID", "Name", "Age", "Email"]
                row = [user.id, user.name, user.age, user.email]
                col_widths = [len(h) for h in headers]
                for i, val in enumerate(row):
                    col_widths[i] = max(col_widths[i], len(str(val)))
                top = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
                mid = "+" + "+".join("=" * (w + 2) for w in col_widths) + "+"
                bottom = top
                print(f"\n{GREEN}✅ User saved successfully!{RESET}")
                print(top)
                print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |")
                print(mid)
                print("| " + " | ".join(str(v).ljust(w) for v, w in zip(row, col_widths)) + " |")
                print(bottom)
            except ValueError as e:
                print(f"\n{RED}❌ Error: {e}{RESET}")


        elif choice == "show":
            CYAN = "\033[96m"
            BOLD = "\033[1m"
            DIM = "\033[2m"
            RESET = "\033[0m"

            users = get_all_users()
            print(f"\n{CYAN}{BOLD}📋 Show All Users{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            if not users:
                print("ℹ️ No users found")
            else:
                headers = ["ID", "Name", "Age", "Email"]
                # Get data from User objects
                data = [[u.id, u.name, u.age, u.email] for u in users]
                # Calculate column widths
                col_widths = [len(h) for h in headers]
                for row in data:
                    for i, val in enumerate(row):
                        col_widths[i] = max(col_widths[i], len(str(val)))
                # Print table
                print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
                print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |")
                print("+" + "+".join("=" * (w + 2) for w in col_widths) + "+")
                for row in data:
                    print("| " + " | ".join(str(v).ljust(w) for v, w in zip(row, col_widths)) + " |")
                print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")


        elif choice == "delete":
            CYAN = "\033[96m"
            RED = "\033[91m"
            GREEN = "\033[92m"
            BOLD = "\033[1m"
            RESET = "\033[0m"
            print(f"\n{CYAN}{BOLD}🗑️ Delete User{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            try:
                user_id = int(input(f" {BOLD}Enter User ID to delete: {RESET}").strip())
                # 1. Fetch the user first
                cursor.execute("SELECT id, name, age, email FROM users WHERE id =?", (user_id,))
                row = cursor.fetchone()
                if row:
                    # 2. Show the user in a table before deleting
                    headers = ["ID", "Name", "Age", "Email"]
                    col_widths = [len(h) for h in headers]
                    for i, val in enumerate(row):
                        col_widths[i] = max(col_widths[i], len(str(val)))
                    top = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
                    mid = "+" + "+".join("=" * (w + 2) for w in col_widths) + "+"
                    bottom = top
                    print(f"\n{GREEN}✅ User {user_id} deleted successfully!{RESET}")
                    print(f"\n{RED}⚠️ About to delete this user:{RESET}")
                    print(top)
                    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |")
                    print(mid)
                    print("| " + " | ".join(str(v).ljust(w) for v, w in zip(row, col_widths)) + " |")
                    print(bottom)
                    # 3. Delete after showing
                    cursor.execute("DELETE FROM users WHERE id =?", (user_id,))
                    conn.commit()
                else:
                    print(f"\n{RED}❌ No user found with ID {user_id}{RESET}")
            except ValueError:
                print(f"\n{RED}❌ Invalid ID. Enter a number.{RESET}")

        elif choice == "update":
            CYAN = "\033[96m"
            YELLOW = "\033[93m"
            GREEN = "\033[92m"
            RED = "\033[91m"
            BOLD = "\033[1m"
            RESET = "\033[0m"

            print(f"\n{CYAN}{BOLD}✏️ Update User{RESET}")
            print(f"{CYAN}─────────────────────{RESET}")
            try:
                user_id = int(input(f" {BOLD}Enter User ID to update: {RESET}").strip())

                # Get old data
                cursor.execute("SELECT id, name, age, email FROM users WHERE id =?", (user_id,))
                old_row = cursor.fetchone()

                if not old_row:
                    print(f"\n{RED}❌ No user found with ID {user_id}{RESET}")
                else:
                    # Show old data
                    headers = ["ID", "Name", "Age", "Email"]
                    print(f"\n{YELLOW}Old Data:{RESET}")
                    print_table([old_row], headers)

                    # Get new data
                    print(f"\n{BOLD}Enter new values. Press Enter to keep current value:{RESET}")
                    new_name = input(f" Name [{old_row[1]}]: ").strip() or old_row[1]
                    new_age = input(f" Age [{old_row[2]}]: ").strip() or str(old_row[2])
                    new_email = input(f" Email [{old_row[3]}]: ").strip() or old_row[3]

                    try:
                        new_age = int(new_age)
                        if new_age < 0:
                            raise ValueError("Age can't be negative")

                        # Update
                        if update_user(user_id, new_name, new_age, new_email):
                            # Get updated data
                            cursor.execute("SELECT id, name, age, email FROM users WHERE id =?", (user_id,))
                            new_row = cursor.fetchone()

                            print(f"\n{GREEN}✅ User updated successfully!{RESET}")
                            print(f"\n{GREEN}New Data:{RESET}")
                            print_table([new_row], headers)
                        else:
                            print(f"\n{RED}❌ Update failed{RESET}")

                    except ValueError as e:
                        print(f"\n{RED}❌ Error: {e}{RESET}")

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
            print(f"{CYAN}║{RESET}  {GREEN}{BOLD}👋 {msg}{RESET} {CYAN} ║{RESET}")
            print(f"{CYAN}╚{'═' * width}╝{RESET}")
            break
        else:
            print("❌ Invalid input. Try again.")

    conn.close()

if __name__ == '__main__':
    main()


