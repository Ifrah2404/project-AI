import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Reports:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=self.app.colors["background"])
        
        # Title
        self.title = tk.Label(
            self.frame,
            text="Expense Reports",
            font=("Arial", 20, "bold"),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        )
        self.title.pack(pady=20)
        
        # Report type selection
        self.report_type = tk.StringVar(value="category")
        
        report_frame = tk.Frame(self.frame, bg=self.app.colors["background"])
        report_frame.pack(pady=10)
        
        tk.Radiobutton(
            report_frame,
            text="By Category",
            variable=self.report_type,
            value="category",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            command=self.generate_reports
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            report_frame,
            text="Daily Expenses",
            variable=self.report_type,
            value="daily",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            command=self.generate_reports
        ).pack(side=tk.LEFT, padx=10)
        
        # Time period selection
        period_frame = tk.Frame(self.frame, bg=self.app.colors["background"])
        period_frame.pack(pady=10)
        
        tk.Label(
            period_frame,
            text="Time Period:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).pack(side=tk.LEFT)
        
        self.period_var = tk.StringVar(value="month")
        periods = [
            ("Last 7 Days", "week"),
            ("This Month", "month"),
            ("Last 3 Months", "3months"),
            ("This Year", "year")
        ]
        
        for text, value in periods:
            tk.Radiobutton(
                period_frame,
                text=text,
                variable=self.period_var,
                value=value,
                font=("Arial", 12),
                bg=self.app.colors["background"],
                command=self.generate_reports
            ).pack(side=tk.LEFT, padx=5)
        
        # Graph frame
        self.graph_frame = tk.Frame(self.frame, bg=self.app.colors["background"])
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def generate_reports(self):
        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Get data based on selected period
        start_date = self.get_start_date()
        
        conn = sqlite3.connect("data/expenses.db")
        cursor = conn.cursor()
        
        try:
            if self.report_type.get() == "category":
                # Category report
                cursor.execute("""
                    SELECT category, SUM(amount) 
                    FROM expenses 
                    WHERE user_id = ? AND date >= ?
                    GROUP BY category
                    ORDER BY SUM(amount) DESC
                """, (self.app.current_user["id"], start_date))
                
                data = cursor.fetchall()
                categories = [item[0] for item in data]
                amounts = [item[1] for item in data]
                
                # Create pie chart
                fig = Figure(figsize=(6, 5), dpi=100)
                ax = fig.add_subplot(111)
                ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
                ax.set_title("Expenses by Category")
                
            else:
                # Daily expenses report
                cursor.execute("""
                    SELECT date, SUM(amount) 
                    FROM expenses 
                    WHERE user_id = ? AND date >= ?
                    GROUP BY date
                    ORDER BY date
                """, (self.app.current_user["id"], start_date))
                
                data = cursor.fetchall()
                dates = [item[0] for item in data]
                amounts = [item[1] for item in data]
                
                # Create bar chart
                fig = Figure(figsize=(8, 5), dpi=100)
                ax = fig.add_subplot(111)
                ax.bar(dates, amounts, color=self.app.colors["primary"])
                ax.set_title("Daily Expenses")
                ax.set_xlabel("Date")
                ax.set_ylabel("Amount ($)")
                ax.tick_params(axis='x', rotation=45)
            
            # Embed the figure in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        finally:
            conn.close()
    
    def get_start_date(self):
        period = self.period_var.get()
        today = datetime.now().date()
        
        if period == "week":
            return (today - timedelta(days=7)).strftime("%Y-%m-%d")
        elif period == "month":
            return today.replace(day=1).strftime("%Y-%m-%d")
        elif period == "3months":
            return (today.replace(day=1) - timedelta(days=60)).strftime("%Y-%m-%d")
        elif period == "year":
            return today.replace(month=1, day=1).strftime("%Y-%m-%d")
        else:
            return "2000-01-01"  # All time