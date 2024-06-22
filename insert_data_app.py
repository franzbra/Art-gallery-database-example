# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:53:12 2024

@author: Francesco Brandoli
"""
# modify_table_tkinter.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db_connection import get_connection

class ModifyTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modify Table")
        
        # Entry fields for table name and columns
        self.table_label = tk.Label(root, text="Enter table name:")
        self.table_label.pack()
        self.table_name_entry = tk.Entry(root)
        self.table_name_entry.pack()
        
        self.column_labels = []
        self.column_entries = []

        self.submit_button = tk.Button(root, text="Insert", command=self.insert_into_table)
        self.submit_button.pack()

    def insert_into_table(self):
        table_name = self.table_name_entry.get().strip()
        
        try:
            cnx, cursor = get_connection()

            # Fetch table columns to display for user guidance
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [column[0] for column in cursor.fetchall()]

            # Create entry fields for each column
            for column in columns:
                label = tk.Label(self.root, text=f"Enter value for {column}:")
                label.pack()
                self.column_labels.append(label)

                entry = tk.Entry(self.root)
                entry.pack()
                self.column_entries.append(entry)

            # Submit button to execute the insert
            self.submit_button.config(state=tk.DISABLED)
            submit_values_button = tk.Button(self.root, text="Submit", command=self.submit_values)
            submit_values_button.pack()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

    def submit_values(self):
        table_name = self.table_name_entry.get().strip()
        column_values = {}

        # Gather values from entry fields
        for i, column in enumerate(self.column_labels):
            column_name = column.cget("text").replace("Enter value for ", "").replace(":", "")
            column_value = self.column_entries[i].get().strip()
            column_values[column_name] = column_value

        try:
            cnx, cursor = get_connection()

            # Prepare the SQL query
            placeholders = ', '.join(['%s'] * len(column_values))
            columns = ', '.join(column_values.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Execute the query
            cursor.execute(sql, tuple(column_values.values()))

            # Commit the transaction
            cnx.commit()

            messagebox.showinfo("Success", f"Inserted into {table_name} successfully.")

            # Clear entry fields
            self.table_name_entry.delete(0, tk.END)
            for entry in self.column_entries:
                entry.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        finally:
            # Enable the submit button again
            self.submit_button.config(state=tk.NORMAL)

            # Close the cursor and connection
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'cnx' in locals() and cnx is not None:
                cnx.close()


if __name__ == '__main__':
    root = tk.Tk()
    app = ModifyTableApp(root)
    root.mainloop()
