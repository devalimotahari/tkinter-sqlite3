from tkinter import ttk
from tkinter import *
from tkinter.messagebox import askyesno

import sqlite3

class Student:
    # connection dir property
    db_name = 'students.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('نمرات دانش آموزان')

        # Name Input
        Label(text = 'نام: ').grid(row = 1, column = 0)
        self.name = Entry()
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Age Input
        Label(text = 'سن: ').grid(row = 2, column = 0)
        self.age = Entry()
        self.age.grid(row = 2, column = 1)


        # Score Input
        Label(text = 'نمره: ').grid(row = 3, column = 0)
        self.score = Entry()
        self.score.grid(row = 3, column = 1)

        # Button Add Student 
        ttk.Button(text = 'ذخیره', command = self.add_student).grid(row = 4, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 5, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns=("name","age","score"))
        self.tree.grid(row = 6, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'شناسه', anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=50, stretch=NO, anchor=CENTER)
        self.tree.heading('name', text = 'نام', anchor = CENTER)
        self.tree.column("name", minwidth=0, width=150, stretch=NO, anchor=CENTER)
        self.tree.heading('age', text = 'سن', anchor = CENTER)
        self.tree.column("age", minwidth=0, width=50, stretch=NO, anchor=CENTER)
        self.tree.heading('score', text = 'نمره', anchor = CENTER)
        self.tree.column("score", minwidth=0, width=80, stretch=NO, anchor=CENTER)

        # Buttons
        ttk.Button(text = 'حذف', command = self.delete_confirm_dialog).grid(row = 7, column = 0, sticky = W + E)
        ttk.Button(text = 'ویرایش', command = self.edit_student).grid(row = 7, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_students()

    def delete_confirm_dialog(self):
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'لطفا یک مورد را انتخاب کنید'
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        answer = askyesno(title='confirmation',
                    message='مطمئنی میخوای ' + name + ' رو پاک کنی؟ ')
        if answer:
            self.delete_student()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Students from Database
    def get_students(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM student ORDER BY id ASC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1],row[2],row[3]))

    # User Input Validation
    def validation(self):
        if(len(self.name.get()) == 0 or len(self.age.get()) == 0 or len(self.score.get()) == 0):
            self.message['text'] = 'لطفا تمامی موارد را کامل کنید'
            return False
        
        if(float(self.score.get()) > 20.0):
            self.message['text'] = 'نمره باید کمتر یا برابر با 20 باشد'
            return False
        
        return True

    def add_student(self):
        if self.validation():
            query = 'INSERT INTO student VALUES(NULL, ?, ?, ?)'
            parameters =  (self.name.get(), self.age.get(), self.score.get())
            self.run_query(query, parameters)
            self.message['text'] = 'دانش آموز با نام {} اضافه شد.'.format(self.name.get())
            self.name.delete(0, END)
            self.score.delete(0, END)

        self.get_students()

    def delete_student(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'لطفا یک مورد را انتخاب کنید'
            return
        self.message['text'] = ''
        id = self.tree.item(self.tree.selection())['text']
        name = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM student WHERE id = ?'

        self.run_query(query, (str(id)))
        self.message['text'] = 'دانش آموز با نام {} حذف شد.'.format(name)
        self.get_students()

    def edit_student(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'لطفا یک مورد را انتخاب کنید'
            return
        studentId = self.tree.item(self.tree.selection())['text'] 
        old_name = self.tree.item(self.tree.selection())['values'][0]
        old_age = self.tree.item(self.tree.selection())['values'][1]
        old_score = self.tree.item(self.tree.selection())['values'][2]

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'ویرایش'

        # New Name
        Label(self.edit_wind, text = 'نام:').grid(row = 0, column = 1)
        new_name = Entry(self.edit_wind,textvariable = StringVar(self.edit_wind, value = old_name))
        new_name.grid(row = 0, column = 2)

        # New Age
        Label(self.edit_wind, text = 'سن:').grid(row = 1, column = 1)
        new_age= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_age))
        new_age.grid(row = 1, column = 2)

        # New Score
        Label(self.edit_wind, text = 'نمره:').grid(row = 2, column = 1)
        new_score= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_score))
        new_score.grid(row = 2, column = 2)

        Button(self.edit_wind, text = 'ویرایش', command = lambda: self.edit_records(studentId, new_name.get(), new_age.get(), new_score.get())).grid(row = 3, column = 1,columnspan=2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self,studentId, new_name, new_age, new_score):
        query = 'UPDATE student SET name = ?, age = ?, score = ? WHERE id = ?'
        parameters = (new_name, new_age, new_score, studentId)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'دانش آموز ویرایش شد'
        self.get_students()

if __name__ == '__main__':
    window = Tk()
    application = Student(window)
    window.mainloop()
