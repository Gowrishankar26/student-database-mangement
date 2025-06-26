import csv
import sqlite3
from itertools import count


class StudentDataBase:
    def __init__(self):
        self.con=sqlite3.connect("student.db")
        self.cursor=self.con.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS student(roll INTEGER PRIMARY KEY,name TEXT NOT NULL,
marks REAL NOT NULL,grade TEXT NOT NULL)''')
        self.con.commit()


    def calculate_grade(self,marks):
        if marks >=90:
            return 'A'
        elif marks >=75:
            return 'B'
        elif marks >=60:
            return 'C'
        elif marks >=40:
            return 'D'
        else:
            return 'F'
    def add_student(self):
        try:
            roll=int(input("Enter the rollno : "))
            name=input("Enter the name : ")
            marks=float(input("Enter the marks : "))
            grade=self.calculate_grade(marks)
            self.cursor.execute("INSERT INTO student(roll,name,marks,grade)VALUES(?,?,?,?)",(roll,name,marks,grade))
            self.con.commit()
            print("Student added sucessfully...")
        except sqlite3.IntegrityError:
            print("Roll number already exists1\n")
        except ValueError:
            print("Invalid Input ,Please Enter Numbers for Roll and marks\n")
    def view_all_student(self):
        self.cursor.execute("SELECT * FROM student")
        rows=self.cursor.fetchall()
        if not rows:
            print("No student record found.\n")
            return
        print("\n Student records:")
        print("Rollno\tName\t\tmarks\tGrade")
        print("-"*40)
        for row in rows:
            print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t{row[3]}")
        print()
    def search_student(self):
        print("search by:")
        print("1.Roll number")
        print("2.Name(partial or full name)")
        choice=input("Enter your choice(1 or 2): ")
        if choice=='1':
            try:
                roll=int(input("enter the rollno: "))
                self.cursor.execute("SELECT * FROM student WHERE roll=?",(roll,))
            except ValueError:
                print("Invalid roll number.\n")
        elif choice=='2':
                name=input("enter the name: ")
                self.cursor.execute("SELECT * FROM student WHERE name LIKE ?", ('%' + name + '%',))

        else:
            print("Invalid choice")
            return
        rows=self.cursor.fetchall()
        if rows:
            print("\n Matching Student :")
            print("Rollno\tName\t\tmarks\tGrade")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t{row[3]}")
        else:
            print("No Student found.\n")
        print()
    def delete_student(self):
        try:
            roll=int(input("Enter the roll number to delete: "))
            self.cursor.execute("SELECT * FROM student WHERE roll=?",(roll,))
            student=self.cursor.fetchone()
            if student:
                self.cursor.execute("DELETE FROM student WHERE roll=?",(roll,))
                self.con.commit()
                print("Student delete Successfully.\n")
            else:
                print("Student not found.\n")
        except ValueError:
            print("Invalid roll Number.\n")
    def update_student(self):
        try:
            roll=int(input("Enter the rool number to update:"))
            self.cursor.execute("SELECT * FROM student WHERE roll=?",(roll,))
            student=self.cursor.fetchone()
            if student:
                print(f"Current Name:{student[1]},Marks:{student[2]},Grade:{student[3]}")
                new_name=input("Enter the new name (press Enter to keep curent name:") or student[1]
                marks_input=input("Enter the new marks (press Enter to keep curent ")
                new_marks=float(marks_input) if marks_input else student[2]
                new_grade=self.calculate_grade(new_marks)
                self.cursor.execute("UPDATE student SET name=?,marks=?,grade=? WHERE roll=?",(new_name,new_marks,new_grade,roll))
                self.con.commit()
                print("Student updated successfully.\n")
            else:
                print("Student not found.\n")
        except ValueError:
            print("Invalid Input")
    def sort_student(self):
        print("Sort student by:")
        print("1.Roll Number")
        print("2.Name")
        print("3.marks")
        print("4.Grade")
        choice=input("Enter  your choice(1-4): ")
        if choice=='1':
            self.cursor.execute("SELECT * FROM student ORDER BY roll ASC")
        elif choice=='2':
            self.cursor.execute("SELECT * FROM student ORDER BY name ASC")
        elif choice=='3':
            self.cursor.execute("SELECT * FROM student ORDER BY marks DESC")
        elif choice=='4':
            self.cursor.execute("SELECT * FROM student ORDER BY grade ASC")
        else:
            print("Ivalid choice")
            return
        rows=self.cursor.fetchall()
        if rows:
            print("\n Sorted  Student :")
            print("Rollno\tName\t\t\tmarks\tGrade")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t\t\t{row[2]}\t{row[3]}")
        else:
            print("No Student found.\n")
        print()
    def admin_login(self):
        print("Admin login")
        username=input("Enter the username:")
        password=input("Enter the password:")
        if username=="admin" and password=="1234":
            print("login successfully")
            return True
        else:
            print("Invalid password not allowed.")
            return False
    def csv_file(self):
        self.cursor.execute("SELECT * FROM student")
        rows=self.cursor.fetchall()
        if not rows:
            print("No student records to export.")
            return
        with open("student.csv","w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(['Roll','Name','Marks','Grade'])
            writer.writerow(rows)
            print("Export successfully! File saved successfully.")

    def analyzer_marks(self):
        self.cursor.execute("SELECT COUNT(*), AVG(marks), MAX(marks), MIN(marks) FROM student")
        result = self.cursor.fetchone()  # fetchone returns a tuple
        count, avg, max_marks, min_marks = result

        if count == 0:
            print("No Student Record to Analyze.")
            return

        self.cursor.execute("SELECT name, marks FROM student WHERE marks=?", (max_marks,))
        topper = self.cursor.fetchone()

        self.cursor.execute("SELECT COUNT(*) FROM student WHERE marks >= 40")
        passed = self.cursor.fetchone()[0]

        failed = count - passed
        pass_percentage = (passed / count) * 100

        print("\nMarks Analysis Report")
        print("-" * 30)
        print(f"Total students           : {count}")
        print(f"Average marks            : {avg:.2f}")
        print(f"Highest marks            : {max_marks}")
        print(f"Lowest marks             : {min_marks}")
        print(f"Topper                   : {topper[0]} ({topper[1]} marks)")
        print(f"Failed students          : {failed}")
        print(f"Pass Percentage          : {pass_percentage:.2f}%")

    def close(self):
        self.con.close()



def main():
    temp = StudentDataBase()
    if not temp.admin_login():
        return
    db = temp
    #db=StudentDataBase()
    while True:
        print("===== STUDENT RECORD MANAGEMENT ======")
        print("1.Add Student")
        print("2.View All Student")
        print("3.Search Student")
        print("4.Delete student")
        print("5.Upadte student")
        print("6.sort student")
        print("7.Export to CSV")
        print("8.Analyze Marks")
        print("9.exit")
        choice=input("Enter your choice: ")
        if choice=='1':
            db.add_student()
        elif choice=='2':
            db.view_all_student()
        elif choice == '3':
            db.search_student()
        elif choice == '4':
            db.delete_student()
        elif choice == '5':
            db.update_student()
        elif choice == '6':
            db.sort_student()
        elif choice == '7':
            db.csv_file()
        elif choice == '8':
            db.analyzer_marks()
        elif choice=='9':
            print("Exiting......")
            db.close()
            break
        else:
            print("invalid choice!")
if __name__=="__main__":
    main()
