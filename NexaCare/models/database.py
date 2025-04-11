import mariadb
import hashlib
import datetime

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'nexacare'
        self.user = 'nexacare_user'
        self.password = 'axeljohn123'
        self.connection = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=3306,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        print("Database connection established.")
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INT AUTO_INCREMENT,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    PRIMARY KEY (id)
                )
            ''')
            self.connection.commit()
            print("Table 'accounts' created or already exists.")
        except mariadb.Error as e:
            print(f"Error creating table: {e}")

    def generate_username(self, role):
        year = datetime.datetime.now().year
        prefix = "H" if role.lower() == "hr" else "D"
        self.cursor.execute(
            "SELECT COUNT(*) FROM accounts WHERE role = ?", (role.lower(),)
        )
        count = self.cursor.fetchone()[0] + 1
        return f"{year}{prefix}{count:04d}"

    def add_user(self, name, password, role):
        if role.lower() not in ["doctor", "hr"]:
            raise ValueError("Invalid role. Allowed values are 'doctor' or 'hr'.")

        try:
            username = self.generate_username(role)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            print(f"Attempting to add user: username={username}, name={name}, role={role}")
            self.cursor.execute(
                "INSERT INTO accounts (username, password, role, name) VALUES (?, ?, ?, ?)",
                (username, hashed_password, role.lower(), name)
            )
            self.connection.commit()
            print(f"User '{name}' added successfully with username '{username}' and role '{role}'.")
            return username
        except mariadb.IntegrityError:
            print(f"Error: Username already exists.")
            raise ValueError("Username already exists.")
        except mariadb.Error as e:
            print(f"Error adding user: {e}")
            self.connection.rollback()
            raise e