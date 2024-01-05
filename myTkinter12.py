import tkinter as tk
import sqlite3
from tkinter import messagebox

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD @imdevana")
        root.configure(bg='dark slate gray')
        root.geometry('380x600')

        # Create a database or connect to an existing one
        self.conn = sqlite3.connect("school.db")
        self.cursor = self.conn.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            stclass TEXT,
            marks REAL
        )''')
        self.conn.commit()

        # Create GUI elements
        self.name_label = tk.Label(root, bg='dark slate gray', text="Name: (Johnny or Alexa)")
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.position_label = tk.Label(root, bg='dark slate gray', text="Class: (XI or IIV)")
        self.position_label.pack()

        self.stclass_entry = tk.Entry(root)
        self.stclass_entry.pack()

        self.salary_label = tk.Label(root, bg='dark slate gray', text="Marks: (95 or 55)")
        self.salary_label.pack()

        self.marks_entry = tk.Entry(root)
        self.marks_entry.pack()

        self.name1_label = tk.Label(root, bg='dark slate gray', text="  ")
        self.name1_label.pack()


        self.add_button = tk.Button(root, text="Add Student", command=self.add_student, bg='dark green', activebackground='green')
        self.add_button.pack()


        self.name1_label = tk.Label(root, bg='dark slate gray', text="  ")
        self.name1_label.pack()


        self.student_listbox = tk.Listbox(root)
        self.student_listbox.pack()

        self.load_students()


        self.name1_label = tk.Label(root, bg='dark slate gray', text="  ")
        self.name1_label.pack()


        self.update_button = tk.Button(root, bg='yellow4', activebackground='yellow', text="Update Student", command=self.update_student)
        self.update_button.pack()


        self.name1_label = tk.Label(root, bg='dark slate gray', text="  ")
        self.name1_label.pack()


        self.delete_button = tk.Button(root, bg='red4', activebackground='red', text="Delete Student", command=self.delete_student)
        self.delete_button.pack()

    def add_student(self):
        name = self.name_entry.get()
        stclass = self.stclass_entry.get()
        marks = self.marks_entry.get()
        if name and stclass and marks:
            #self.cursor.execute("INSERT INTO students (name, class, marks) VALUES (?, ?, ?)", (name, class, marks))
            self.cursor.execute("INSERT INTO students (name, stclass, marks) VALUES (?, ?, ?)", (name, stclass, marks))
            self.conn.commit()
            self.load_students()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def load_students(self):
        self.student_listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()
        for row in students:
            self.student_listbox.insert(tk.END, f"{row[0]}. {row[1]}, {row[2]}, {'%.2f' % float(row[3])}")


    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.stclass_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    def update_student(self):
        selected_student = self.student_listbox.get(tk.ACTIVE)
        if selected_student:
            student_id = int(selected_student.split(".")[0])
            name = self.name_entry.get()
            stclass = self.stclass_entry.get()
            marks = self.marks_entry.get()
            if name and stclass and marks:
                self.cursor.execute("UPDATE students SET name=?, stclass=?, marks=? WHERE id=?", (name, stclass, marks, student_id))
                self.conn.commit()
                self.load_students()
                self.clear_entries()
            else:
                messagebox.showwarning("Warning", "Please fill in all fields.")
        else:
            messagebox.showwarning("Warning", "Please select an student to update.")

    def delete_student(self):
        selected_student = self.student_listbox.get(tk.ACTIVE)
        if selected_student:
            student_id = int(selected_student.split(".")[0])
            self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            self.conn.commit()
            self.load_students()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Please select an student to delete.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
