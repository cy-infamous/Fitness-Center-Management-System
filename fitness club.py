import pickle
import random
import csv
from datetime import datetime
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='cherry',
    db='fitnesspy'
)

class FitnessCenter:
    def __init__(self):
        self.connection = connection
        self.create_tables()
        self.sample_classes = [
            {'class_id': 'C001', 'class_name': 'Yoga', 'trainer_id': 'T001', 'schedule_time': '2024-10-01 10:00'},
            {'class_id': 'C002', 'class_name': 'Pilates', 'trainer_id': 'T002', 'schedule_time': '2024-10-01 11:00'},
            {'class_id': 'C003', 'class_name': 'Zumba', 'trainer_id': 'T003', 'schedule_time': '2024-10-01 12:00'},
            {'class_id': 'C004', 'class_name': 'Kickboxing', 'trainer_id': 'T004', 'schedule_time': '2024-10-01 13:00'},
            {'class_id': 'C005', 'class_name': 'Spin Class', 'trainer_id': 'T005', 'schedule_time': '2024-10-01 14:00'},
        ]

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    member_id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255),
                    password VARCHAR(255),
                    membership_status VARCHAR(50),
                    attendance TEXT,
                    payments TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trainers (
                    trainer_id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    specialty VARCHAR(255),
                    classes TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    class_id VARCHAR(255) PRIMARY KEY,
                    class_name VARCHAR(255),
                    trainer_id VARCHAR(255),
                    schedule_time DATETIME,
                    feedback TEXT,
                    is_canceled BOOLEAN DEFAULT FALSE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    class_id VARCHAR(255),
                    member_id VARCHAR(255),
                    PRIMARY KEY (class_id, member_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    member_id VARCHAR(255),
                    amount DECIMAL(10, 2),
                    payment_date DATETIME,
                    PRIMARY KEY (member_id, payment_date)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                    class_id VARCHAR(255),
                    member_id VARCHAR(255),
                    feedback_text TEXT,
                    feedback_date DATETIME
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INT AUTO_INCREMENT PRIMARY KEY,
                    class_id VARCHAR(255),
                    member_id VARCHAR(255),
                    rating INT,
                    review_text TEXT,
                    review_date DATETIME
                )
            """)
            self.connection.commit()
            print("Tables created successfully.")

    def register_member(self, name, email, password):
        member_id = email  # Using email as member_id for simplicity
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO members (member_id, name, email, password, membership_status, attendance, payments)
                    VALUES (%s, %s, %s, %s, 'active', '', '')
                """, (member_id, name, email, password))
                self.connection.commit()
                print(f"Welcome {name}! You have registered successfully.")
                self.user_menu(member_id, name)  # Pass the member_id and name to the user menu
        except pymysql.MySQLError as e:
            print(f"Error registering member: {e}")

    def login_member(self, email, password):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT member_id, name FROM members WHERE email = %s AND password = %s
            """, (email, password))
            result = cursor.fetchone()
            if result:
                member_id, member_name = result
                print(f"Welcome back, {member_name}!")
                return member_id, member_name  # Return both member_id and member_name
            else:
                print("Invalid email or password.")
                return None, None  # Return None if login fails

    def admin_login(self, username, password):
        if username == "kartik" and password == "kartik23":
            print("Welcome to the Admin Panel!")
            return True
        else:
            print("Invalid admin credentials.")
            return False

    def user_menu(self, member_id, member_name):
        while True:
            print("\nUser Menu:")
            print("1. View Profile")
            print("2. Update Profile")
            print("3. View Available Classes")
            print("4. View Class Schedule")
            print("5. Register for Class")
            print("6. Track Attendance")
            print("7. Process Payment")
            print("8. Collect Feedback")
            print("9. Leave a Review")
            print("10. View Payment History")
            print("11. Cancel Class Registration")
            print("12. Logout")
            choice = input("Choose an option: ")
            if choice == '1':
                self.view_profile(member_id)  # Use member_id to view profile
            elif choice == '2':
                member_name = self.update_profile(member_name)  # Update name and reflect it
            elif choice == '3':
                self.view_available_classes()  # Display available classes
            elif choice == '4':
                self.view_class_schedule()  # View class schedule
            elif choice == '5':
                class_id = input("Enter class ID to register: ")
                self.register_for_class(member_id, class_id)
            elif choice == '6':
                class_id = input("Enter class ID to track attendance: ")
                self.track_attendance(member_id, class_id)  # Track attendance
            elif choice == '7':
                amount = float(input("Enter payment amount: "))
                self.process_payment(member_id, amount)  # Process payment
            elif choice == '8':
                feedback_text = input("Enter your feedback: ")
                self.collect_feedback(member_id, feedback_text)
            elif choice == '9':
                class_id = input("Enter class ID for review: ")
                rating = int(input("Enter your rating (1-5): "))
                review_text = input("Enter your review: ")
                self.collect_review(member_id, class_id, rating, review_text)
            elif choice == '10':
                self.view_payment_history(member_id)  # View payment history
            elif choice == '11':
                class_id = input("Enter class ID to cancel registration: ")
                self.cancel_class_registration(member_id, class_id)
            elif choice == '12':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_menu(self):
        while True:
            print("\nAdmin Menu:")
            print("1. View All Members")
            print("2. View All Classes")
            print("3. Add Class")
            print("4. Update Class")
            print("5. Remove Class")
            print("6. View Attendance Report")
            print("7. Logout")
            choice = input("Choose an option: ")
            if choice == '1':
                self.view_all_members()
            elif choice == '2':
                self.view_all_classes()  # Display all classes for admin
            elif choice == '3':
                self.add_class()
            elif choice == '4':
                self.update_class()
            elif choice == '5':
                class_id = input("Enter class ID to remove: ")
                self.remove_class(class_id)
            elif choice == '6':
                self.view_attendance_report()
            elif choice == '7':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_class_schedule(self):
        print("\nClass Schedule:")
        for class_ in self.sample_classes:
            print(f"Class ID: {class_['class_id']}, Name: {class_['class_name']}, Trainer ID: {class_['trainer_id']}, Schedule: {class_['schedule_time']}")

    def toggle_user_status(self, email):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT membership_status FROM members WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                new_status = 'inactive' if result[0] == 'active' else 'active'
                cursor.execute("UPDATE members SET membership_status = %s WHERE email = %s", (new_status, email))
                self.connection.commit()
                print(f"User {email} has been {'deactivated' if new_status == 'inactive' else 'reactivated'}.")
            else:
                print("User not found.")

    def generate_user_activity_report(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT member_id, COUNT(class_id) as classes_attended FROM attendance GROUP BY member_id
            """)
            report = cursor.fetchall()
            print("User Activity Report:")
            for record in report:
                print(f"Member ID: {record[0]}, Classes Attended: {record[1]}")

    def view_profile(self, member_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT name, email FROM members WHERE member_id = %s
            """, (member_id,))
            profile = cursor.fetchone()
            if profile is None:
                print("Profile not found.")
                return
            print(f"Profile Information: Name: {profile[0]}, Email: {profile[1]}")

    def update_profile(self, member_name):
        print("Update Profile")
        new_name = input("Enter your new name (leave blank to keep current): ")
        new_email = input("Enter your new email (leave blank to keep current): ")
        new_password = input("Enter your new password (leave blank to keep current): ")
        with self.connection.cursor() as cursor:
            if new_name:
                cursor.execute("""
                    UPDATE members SET name = %s WHERE member_id = %s
                """, (new_name, member_name))
                member_name = new_name  # Update the member_name variable
            if new_email:
                cursor.execute("""
                    UPDATE members SET email = %s WHERE member_id = %s
                """, (new_email, member_name))
            if new_password:
                cursor.execute("""
                    UPDATE members SET password = %s WHERE member_id = %s
                """, (new_password, member_name))
            self.connection.commit()
            print("Profile updated successfully.")
        return member_name  # Return the updated name

    def view_available_classes(self):
        print("Available Classes:")
        for class_ in self.sample_classes:
            print(f"ID: {class_['class_id']}, Name: {class_['class_name']}, Schedule: {class_['schedule_time']}")

    def register_for_class(self, member_id, class_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO attendance (class_id, member_id)
                VALUES (%s, %s)
            """, (class_id, member_id))
            self.connection.commit()
            print(f"Successfully registered for class ID {class_id}.")

    def track_attendance(self, member_id, class_id):
        # Simulate tracking attendance
        print(f"Attendance tracked for {member_id} in class {class_id}.")

    def process_payment(self, member_id, amount):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO payments (member_id, amount, payment_date)
                VALUES (%s, %s, NOW())
            """, (member_id, amount))
            self.connection.commit()
            print(f"Payment of {amount} processed for {member_id}.")

    def collect_feedback(self, member_id, feedback_text):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO feedback (class_id, member_id, feedback_text, feedback_date)
                VALUES (%s, %s, %s, NOW())
            """, (None, member_id, feedback_text))  # Assuming class_id is optional
            self.connection.commit()
            print(f"Feedback collected from {member_id}: {feedback_text}")

    def collect_review(self, member_id, class_id, rating, review_text):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO reviews (class_id, member_id, rating, review_text, review_date)
                VALUES (%s, %s, %s, %s, NOW())
            """, (class_id, member_id, rating, review_text))
            self.connection.commit()
            print(f"Review collected for class {class_id} from {member_id}.")

    def view_payment_history(self, member_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT amount, payment_date FROM payments WHERE member_id = %s
            """, (member_id,))
            payments = cursor.fetchall()
            print("Payment History:")
            for payment in payments:
                print(f"Amount: {payment[0]}, Date: {payment[1]}")

    def cancel_class_registration(self, member_id, class_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM attendance WHERE class_id = %s AND member_id = %s
            """, (class_id, member_id))
            self.connection.commit()
            print(f"Successfully canceled registration for class ID {class_id}.")

    def add_class(self):
        class_id = input("Enter class ID: ")
        class_name = input("Enter class name: ")
        trainer_id = input("Enter trainer ID: ")
        schedule_time = input("Enter schedule time (YYYY-MM-DD HH:MM): ")
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO classes (class_id, class_name, trainer_id, schedule_time)
                VALUES (%s, %s, %s, %s)
            """, (class_id, class_name, trainer_id, schedule_time))
            self.connection.commit()
            print(f"Class '{class_name}' added successfully.")

    def update_class(self):
        class_id = input("Enter class ID to update: ")
        new_class_name = input("Enter new class name (leave blank to keep current): ")
        new_trainer_id = input("Enter new trainer ID (leave blank to keep current): ")
        new_schedule_time = input("Enter new schedule time (YYYY-MM-DD HH:MM, leave blank to keep current): ")
        with self.connection.cursor() as cursor:
            if new_class_name:
                cursor.execute("""
                    UPDATE classes SET class_name = %s WHERE class_id = %s
                """, (new_class_name, class_id))
            if new_trainer_id:
                cursor.execute("""
                    UPDATE classes SET trainer_id = %s WHERE class_id = %s
                """, (new_trainer_id, class_id))
            if new_schedule_time:
                cursor.execute("""
                    UPDATE classes SET schedule_time = %s WHERE class_id = %s
                """, (new_schedule_time, class_id))
            self.connection.commit()
            print(f"Class ID {class_id} updated successfully.")

    def remove_class(self, class_id):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM classes WHERE class_id = %s
            """, (class_id,))
            self.connection.commit()
            print(f"Class ID {class_id} removed successfully.")

    def view_all_members(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM members")
            members = cursor.fetchall()
            print("All Members:")
            for member in members:
                print(member)

    def view_all_classes(self):
        print("\nAll Classes:")
        for class_ in self.sample_classes:
            print(f"Class ID: {class_['class_id']}, Name: {class_['class_name']}, Trainer ID: {class_['trainer_id']}, Schedule: {class_['schedule_time']}")

    def view_attendance_report(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT class_id, COUNT(member_id) as attendance_count FROM attendance GROUP BY class_id
            """)
            report = cursor.fetchall()
            print("Attendance Report:")
            for record in report:
                print(f"Class ID: {record[0]}, Attendance Count: {record[1]}")

    def close_connection(self):
        self.connection.close()
        print("Database connection closed.")

# Main program
def main():
    fitness_center = FitnessCenter()
    while True:
        print("\nWelcome to the Fitness Center Management System")
        print("1. Register")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            fitness_center.register_member(name, email, password)  # This will now show the user menu after registration
        elif choice == '2':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            member_id, member_name = fitness_center.login_member(email, password)  # Get both member_id and member_name
            if member_id:
                fitness_center.user_menu(member_id, member_name)  # Pass both to user_menu
        elif choice == '3':
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if fitness_center.admin_login(username, password):
                fitness_center.admin_menu()
        elif choice == '4':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")
    fitness_center.close_connection()

if __name__ == "__main__":
    main()