from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime
import pytz

root = Tk()
root.title("My Note")
root.geometry("600x700")
root.resizable(0, 0)
root.configure(bg='black')

IST = pytz.timezone('Europe/Paris')

conn = sqlite3.connect('My_note.db')
c = conn.cursor()
'''
# CREATING A TABLE
c.execute("""CREATE TABLE notes(
        title text,
        note_entry text)
        """)
'''

def save():
    conn = sqlite3.connect('My_note.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes VALUES (:title,:note_entry)",
              {
                  'title': title_entry.get(),
                  'note_entry': note_entry.get("1.0", END)
              })

    conn.commit()
    conn.close()

    title_entry.delete(0, END)
    note_entry.delete(1.0, END)


def display():
    conn = sqlite3.connect('My_note.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM notes")
    records = c.fetchall()
    # print(records)
    print_records = ''

    for note in records:
        title_display_text.delete(1.0, END)
        print_records += str(note[0]) + "\t" \
                         + str(note[2]) + "\n"

        title_display_text.insert(1.0, print_records)

    conn.commit()
    conn.close()


def deleteNote():
    if oid_entry.get() == '':
        messagebox.showerror("Error", "Select ID Number To Delete Your Notes")

    else:
        conn = sqlite3.connect('My_note.db')
        c = conn.cursor()
        c.execute("DELETE from notes WHERE oid=" + oid_entry.get())

        conn.commit()
        conn.close()


def ShowNotes():
    if oid_entry.get() == '':
        messagebox.showerror("Error", "Select ID Number To Read Your Notes")

    else:

        root.withdraw()
        editor = Tk()
        editor.title("Edite Note")
        editor.geometry("600x700")
        editor.resizable(0, 0)
        editor.configure(bg='black')



        def SaveEdited():
            if note_entry_editor.get(1.0, END) and title_entry_editor.get():
                response = messagebox.askyesno("Save", "Are You Sure You Want To Save Edited Version?")
                # print(response)
                if response == True:
                    conn = sqlite3.connect('My_note.db')
                    c = conn.cursor()
                    record_id = oid_entry.get()
                    c.execute("""UPDATE notes SET
                    title = :title,
                    note_entry = :note_entry
                    
                    WHERE oid =:oid""",
                              {
                                  'title': title_entry_editor.get(),
                                  'note_entry': note_entry_editor.get(1.0, END),
                                  'oid': record_id

                              })

                    conn.commit()
                    conn.close()
                    root.deiconify()

                    editor.destroy()

        conn = sqlite3.connect('My_note.db')
        c = conn.cursor()
        recorde_id = oid_entry.get()

        c.execute("SELECT * FROM notes WHERE oid=" + recorde_id)
        records = c.fetchall()

        def update_tym_editory():
            raw_ts_editory = datetime.now(IST)
            date_now_editory = raw_ts_editory.strftime("%d %b %Y")
            time_now_editory = raw_ts_editory.strftime("%H:%M")
            label_date_now_editory.config(text=date_now_editory, bg='black', fg='white')
            label_time_now_editory.config(text=time_now_editory, bg='black', fg='white')
            label_time_now_editory.after(1000, update_tym)

        # Date And Time Live Update
        label_date_now_editory = Label(editor, text='', bg='black', fg='white')
        label_date_now_editory.place(x=479, y=84)

        label_time_now_editory = Label(editor, text='', bg='black', fg='white')
        label_time_now_editory.place(x=440, y=84)

        update_tym_editory()

        title_label_editor = Label(editor, text="My Note", font=('times new roman', 15, "bold"), bg='black', fg='white')
        # title_label.grid(row= 0 , column=0)
        title_label_editor.place(x=300, y=30)

        note_title_editor = Label(editor, text="Title", font=('times new roman', 15, "bold"), bg='black', fg='white')
        note_title_editor.place(x=140, y=80)

        title_entry_editor = Entry(editor, font=('times new roman', 15, "bold"), bg='#ebf6f7')
        title_entry_editor.place(x=225, y=80)

        note_entry_editor = Text(editor, height=19.5, width=60, borderwidth=3, bg='#ebf6f7')
        note_entry_editor.place(x=60, y=130)

        for note in records:
            title_entry_editor.insert(0, note[0]),
            note_entry_editor.insert(1.0, note[1])

        save_btn_editor = Button(editor, text="Save Notes", width=20, command=SaveEdited)
        save_btn_editor.place(x=397, y=475)

        conn.commit()
        conn.close()


def update_tym():
    raw_ts = datetime.now(IST)
    date_now = raw_ts.strftime("%d %b %Y")
    time_now = raw_ts.strftime("%H:%M")
    label_date_now.config(text=date_now, bg='black', fg='white')
    label_time_now.config(text=time_now, bg='black', fg='white')
    label_time_now.after(1000, update_tym)


# Date And Time Live Update
label_date_now = Label(root, text='', bg='black', fg='white')
label_date_now.place(x=479, y=84)

label_time_now = Label(root, text='', bg='black', fg='white')
label_time_now.place(x=440, y=84)


update_tym()

title_label = Label(root, text="My Note", font=('times new roman', 15, "bold"), bg='black', fg='white')
# title_label.grid(row= 0 , column=0)
title_label.place(x=270, y=30)

note_title = Label(root, text="Title", font=('times new roman', 15, "bold"), bg='black', fg='white')
note_title.place(x=140, y=80)

title_entry = Entry(root, font=('times new roman', 15, "bold"), bg='#ebf6f7')
title_entry.place(x=225, y=80)

note_entry = Text(root, height=19.5, width=60, borderwidth=3, bg='#ebf6f7')
note_entry.place(x=60, y=130)

# OID
Select_id_label = Label(text="Select ID", font=('times new roman', 15, "bold"), bg='black', fg='white')
Select_id_label.place(x=60, y=475)
oid_entry = Entry(root, font=('times new roman', 15, "bold"), bg='#ebf6f7')
oid_entry.place(x=150, y=475)

# Buttons
save_btn = Button(root, text="Save Notes", width=20, font=('arial', 9, 'bold'), bg='gray20', fg='white',
                  bd=5, command=save)
save_btn.place(x=390, y=610)
Display_btn = Button(root, text="Show Titles", width=20, font=('arial', 9, 'bold'), bg='gray20', fg='white',
                     bd=5, command=display)
Display_btn.place(x=390, y=475)
Delete = Button(root, text="Delete Notes", width=20, font=('arial', 9, 'bold'), bg='gray20', fg='white',
                bd=5, command=deleteNote)
Delete.place(x=390, y=565)
Show_Notes = Button(root, text="Show Notes", width=20, font=('arial', 9, 'bold'), bg='gray20', fg='white',
                    bd=5, command=ShowNotes)
Show_Notes.place(x=390, y=520)

# Title Display Entry
title_display_text = Text(root, height=7, width=25, bg='#ebf6f7')
title_display_text.place(x=150, y=520)

conn.commit()
conn.close()

root.mainloop()
