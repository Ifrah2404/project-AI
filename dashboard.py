import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta

class Dashboard:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=self.app.colors["background"])
        
        # Create widgets
        self.title = tk.Label(
            self.frame,
            text="Expense Dashboard",
            font=("Arial", 20, "bold"),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        )
        self.title.pack(pady=20)
        
        # Summary cards
        self.summary_frame = tk.Frame(self.frame, bg=self.app.colors["background"])
        self.summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Recent expenses table
        self.expenses_table = ttk.Treeview(
            self.frame,
            columns=("date", "category", "amount", "description"),
            show="headings"
        )
        self.expenses_table.heading("date", text="Date")
        self.expenses_table.heading("category", text="Category")
        self.expenses_table.heading("amount", text="Amount")
        self.expenses_table.heading("description", text="Description")
        self.expenses_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.expenses_table, orient="vertical", command=self.expenses_table.yview)
        self.expenses_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self.refresh()
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def refresh(self):
        # Clear existing data
        for item in self.expenses_table.get_children():
            self.expenses_table.delete(item)
        
        # Get data from database
        conn = sqlite3.connect("data/expenses.db")
        cursor = conn.cursor()
        
        try:
            # Get recent expenses
            cursor.execute("""
                SELECT date, category, amount, description 
                FROM expenses 
                WHERE user_id = ? 
                ORDER BY date DESC 
                LIMIT 50
            """, (self.app.current_user["id"],))
            
            expenses = cursor.fetchall()
            
            # Populate table
            for expense in expenses:
                self.expenses_table.insert("", "end", values=expense)
            
            # Update summary cards
            self.update_summary_cards(cursor)
            
        finally:
            conn.close()
    
    def update_summary_cards(self, cursor):
        # Clear existing summary cards
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # Today's expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM expenses 
            WHERE user_id = ? AND date = ?
        """, (self.app.current_user["id"], datetime.now().strftime("%Y-%m-%d")))
        
        today_expense = cursor.fetchone()[0]
        
        # Monthly expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM expenses 
            WHERE user_id = ? AND strftime('%Y-%m', date) = ?
        """, (self.app.current_user["id"], datetime.now().strftime("%Y-%m")))
        
        monthly_expense = cursor.fetchone()[0]
        
        # Create summary cards
        summary_cards = [
            ("Today", f"${today_expense:.2f}", self.app.colors["primary"]),
            ("This Month", f"${monthly_expense:.2f}", self.app.colors["secondary"])
        ]
        
        for title, value, color in summary_cards:
            card = tk.Frame(
                self.summary_frame,
                bg=color,
                bd=1,
                relief=tk.RAISED,
                padx=10,
                pady=10
            )
            
            title_label = tk.Label(
                card,
                text=title,
                font=("Arial", 12),
                bg=color,
                fg="white"
            )
            title_label.pack()
            
            value_label = tk.Label(
                card,
                text=value,
                font=("Arial", 18, "bold"),
                bg=color,
                fg="white"
            )
            value_label.pack()
            
            card.pack(side=tk.LEFT, padx=10, ipadx=20, ipady=10)