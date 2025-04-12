import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

class AddExpense:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=self.app.colors["background"])
        
        # Form elements
        self.title = tk.Label(
            self.frame,
            text="Add New Expense",
            font=("Arial", 20, "bold"),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        )
        self.title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.frame, bg=self.app.colors["background"])
        form_frame.pack(pady=10)
        
        # Date
        tk.Label(
            form_frame,
            text="Date:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.date_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.date_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Category
        tk.Label(
            form_frame,
            text="Category:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.category_var = tk.StringVar()
        categories = ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Healthcare", "Other"]
        self.category_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=categories,
            font=("Arial", 12),
            state="readonly"
        )
        self.category_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.category_dropdown.current(0)
        
        # Amount
        tk.Label(
            form_frame,
            text="Amount:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.amount_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Description
        tk.Label(
            form_frame,
            text="Description:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).grid(row=3, column=0, padx=10, pady=5, sticky="ne")
        
        self.description_entry = tk.Text(form_frame, height=4, width=30, font=("Arial", 12))
        self.description_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        # Submit button
        submit_btn = tk.Button(
            self.frame,
            text="Add Expense",
            font=("Arial", 12),
            bg=self.app.colors["primary"],
            fg="white",
            command=self.submit_expense
        )
        submit_btn.pack(pady=20)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def submit_expense(self):
        # Get form data
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get("1.0", tk.END).strip()
        
        # Validate
        if not date or not category or not amount:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        
        # Save to database
        conn = sqlite3.connect("data/expenses.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO expenses (user_id, date, category, amount, description)
                VALUES (?, ?, ?, ?, ?)
            """, (self.app.current_user["id"], date, category, amount, description))
            
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully")
            
            # Clear form
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
        finally:
            conn.close()