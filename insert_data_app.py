# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 16:53:12 2024

@author: Francesco Brandoli
"""
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from db_connection import get_connection

class ModifyTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modify Table")
        self.root.geometry("400x300")

        # Define colors
        self.bg_color = "#4CAF50"  # Dark green background
        self.button_color = "#4CAF50"  # Green button color
        self.error_color = "#FF5733"  # Red error color
        self.label_color = "#333333"  # Dark gray label color

        # Set background color
        self.root.configure(background=self.bg_color)

        self.create_widgets()

    def create_widgets(self):
        # Frame for table name input
        table_frame = tk.Frame(self.root, bg=self.bg_color)
        table_frame.pack(pady=20)

        self.table_label = tk.Label(table_frame, text="Enter table name:", bg=self.bg_color, fg=self.label_color)
        self.table_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.table_name_entry = tk.Entry(table_frame, width=30)
        self.table_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Submit button for table name input
        submit_table_button = tk.Button(table_frame, text="Fetch Columns", bg=self.button_color, fg="black",
                                        command=self.fetch_columns)
        submit_table_button.grid(row=0, column=2, padx=10, pady=5)

        # Frame for column inputs
        self.column_frame = tk.Frame(self.root, bg=self.bg_color)
        self.column_frame.pack(pady=20)

        self.column_labels = []
        self.column_entries = {}

        # Submit button for inserting values
        self.submit_button = tk.Button(self.root, text="Insert", bg=self.button_color, fg="black",
                                       command=self.insert_into_table, state=tk.DISABLED)
        self.submit_button.pack()

    def fetch_columns(self):
        table_name = self.table_name_entry.get().strip()

        if not table_name:
            messagebox.showerror("Error", "Please enter a table name.")
            return

        try:
            cnx, cursor = get_connection()

            # Fetch table columns to display for user guidance
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [column[0] for column in cursor.fetchall()]

            # Destroy previous widgets in column_frame
            for widget in self.column_frame.winfo_children():
                widget.destroy()

            # Create entry fields for each column
            self.column_labels = []
            self.column_entries = {}

            for i, column in enumerate(columns):
                label = tk.Label(self.column_frame, text=f"{column}:", bg=self.bg_color, fg=self.label_color)
                label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
                self.column_labels.append(label)

                entry = tk.Entry(self.column_frame, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.column_entries[column] = entry

            # Enable the insert button
            self.submit_button.config(state=tk.NORMAL)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        finally:
            # Close the cursor and connection
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'cnx' in locals() and cnx is not None:
                cnx.close()

    def insert_into_table(self):
        table_name = self.table_name_entry.get().strip()
        column_values = {}

        # Gather values from entry fields
        for column, entry in self.column_entries.items():
            column_value = entry.get().strip()
            if not column_value:
                messagebox.showerror("Error", f"Please enter a value for {column}.")
                return
            column_values[column] = column_value

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
            for entry in self.column_entries.values():
                entry.delete(0, tk.END)

            # Refresh column frame
            self.fetch_columns()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

        finally:
            # Close the cursor and connection
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'cnx' in locals() and cnx is not None:
                cnx.close()


if __name__ == '__main__':
    root = tk.Tk()
    app = ModifyTableApp(root)
    root.mainloop()
