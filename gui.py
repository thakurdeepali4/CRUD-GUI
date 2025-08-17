import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Global states
isUpdateVisible = False
isDeleteVisible = False
update_frame = None
delete_frame = None

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["CollegeData"]
collection = db["students"]

# Main window
app = tk.Tk()
app.title("536- Deepali Ramichand Thakur ")
app.geometry("1000x650")
app.configure(bg="lavender")

# Title
tk.Label(app, text="CRUD Operations", font=("Arial", 16), bg="plum").pack( padx=20, pady=10)

# College ID
tk.Label(app, text="College ID:", bg="plum").pack(padx=20)
id_entry = tk.Entry(app, width=40)
id_entry.pack(padx=20)

# First Name
tk.Label(app, text="First Name:", bg="plum").pack(padx=20)
first_name_entry = tk.Entry(app, width=40)
first_name_entry.pack(padx=20)

# Last Name
tk.Label(app, text="Last Name:", bg="plum").pack(padx=20)
last_name_entry = tk.Entry(app, width=40)
last_name_entry.pack(padx=20)

# Age
tk.Label(app, text="Age:", bg="plum").pack(padx=20)
age_entry = tk.Entry(app, width=40)
age_entry.pack(padx=20)

# Contact Info
tk.Label(app, text="Contact Info:", bg="plum").pack(padx=20)
contact_entry = tk.Entry(app, width=40)
contact_entry.pack(padx=20)


# Insert Function
def insert():
    id = id_entry.get().strip()
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    age = age_entry.get().strip()
    contact = contact_entry.get().strip()

    if not (id and first_name and last_name and age and contact):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    if collection.find_one({"id": id}):
        messagebox.showwarning("Duplicate ID", "A record with this College ID already exists.")
        return

    try:
        collection.insert_one({
            "id": id,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "contact": contact
        })
        messagebox.showinfo("Success", "Data inserted successfully!")
        id_entry.delete(0, tk.END)
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "Failed to insert data.")


# Display Function
def read():
    win = tk.Toplevel(app)
    win.title("Display Records")
    win.geometry("600x400")
    result_label = tk.Label(win, text="", justify="left", anchor="w", bg="lavender")
    result_label.pack(anchor="w", padx=20, pady=10)

    try:
        documents = collection.find()
        result = ""
        for doc in documents:
            result += (
                f"Id: {doc.get('id','')}\n"
                f"First Name: {doc.get('first_name','')}\n"
                f"Last Name: {doc.get('last_name','')}\n"
                f"Age: {doc.get('age','')}\n"
                f"Contact: {doc.get('contact','')}\n\n"
            )
        result_label.config(text=result)
    except:
        messagebox.showerror("Error", "Failed to display data.")


# Update Function
def update():
    global isUpdateVisible, update_frame, delete_frame, isDeleteVisible

    if delete_frame:
        delete_frame.destroy()
        isDeleteVisible = False

    if not isUpdateVisible:
        isUpdateVisible = True
        update_frame = tk.Frame(app, bg="lavender")
        update_frame.pack(padx=20, pady=10)

        id_label = tk.Label(update_frame, text="Enter College ID to Update the document feilds:", bg="lavender")
        id_label.pack(pady=5)
        id_input = tk.Entry(update_frame, width=40)
        id_input.pack(pady=2)

        first_name_label = tk.Label(update_frame, text="Update First Name:", bg="lavender")
        first_name_label.pack(pady=2)
        first_name_input = tk.Entry(update_frame, width=40)
        first_name_input.pack(pady=2)

        last_name_label = tk.Label(update_frame, text="Update Last Name:", bg="lavender")
        last_name_label.pack(pady=2)
        last_name_input = tk.Entry(update_frame, width=40)
        last_name_input.pack(pady=2)

        age_label = tk.Label(update_frame, text="Update Age:", bg="lavender")
        age_label.pack(pady=2)
        age_input = tk.Entry(update_frame, width=40)
        age_input.pack(pady=2)

        contact_label = tk.Label(update_frame, text="Update Contact:", bg="lavender")
        contact_label.pack(pady=2)
        contact_input = tk.Entry(update_frame, width=40)
        contact_input.pack(pady=2)

        def updateinfo():
            global isUpdateVisible
            old_id = id_input.get().strip()
            new_first_name = first_name_input.get().strip()
            new_last_name = last_name_input.get().strip()
            new_age = age_input.get().strip()
            new_contact = contact_input.get().strip()

            if not old_id:
                messagebox.showwarning("Warning", "Please enter the College ID to update the document fields.")
                return

            update_fields = {}
            if new_first_name:
                update_fields["first_name"] = new_first_name
            if new_last_name:
                update_fields["last_name"] = new_last_name
            if new_age:
                update_fields["age"] = new_age
            if new_contact:
                update_fields["contact"] = new_contact

            if not update_fields:
                messagebox.showwarning("Warning", "Please enter at least one field to update.")
                return

            result = collection.update_one({"id": old_id}, {"$set": update_fields})
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Record updated successfully!")
            else:
                messagebox.showinfo("No Match", "No record found.")

            update_frame.destroy()
            isUpdateVisible = False

        tk.Button(update_frame, text="Confirm Update", command=updateinfo).pack(pady=10)

    else:
        update_frame.destroy()
        isUpdateVisible = False


# Delete Function
def delete():
    global isDeleteVisible, delete_frame, update_frame, isUpdateVisible

    if update_frame:
        update_frame.destroy()
        isUpdateVisible = False

    if not isDeleteVisible:
        isDeleteVisible = True
        delete_frame = tk.Frame(app, bg="lavender")
        delete_frame.pack(padx=20, pady=10)

        id_label = tk.Label(delete_frame, text="Enter College ID to delete the document:", bg="lavender")
        id_label.pack(pady=5)
        id_input = tk.Entry(delete_frame, width=40)
        id_input.pack(pady=2)

        def deleteInfo():
            global isDeleteVisible
            old_id = id_input.get().strip()
            if not old_id:
                messagebox.showwarning("Warning", "Please enter a College ID to delete.")
                return

            result = collection.delete_one({"id": old_id})
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showinfo("No Match", "No matching record found.")

            delete_frame.destroy()
            isDeleteVisible = False

        tk.Button(delete_frame, text="Confirm Delete", command=deleteInfo).pack(anchor="w", pady=10)

    else:
        delete_frame.destroy()
        isDeleteVisible = False


# Buttons Frame (centered horizontally)
buttons_frame = tk.Frame(app, bg="lavender")
buttons_frame.pack(pady=30)

tk.Button(buttons_frame, text="Insert", command=insert, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Display Users", command=read, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Update", command=update, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Delete", command=delete, width=15).pack(side=tk.LEFT, padx=10)

# Run app
app.mainloop()