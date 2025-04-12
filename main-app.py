import tkinter as tk
from tkinter import ttk, messagebox
from components.dashboard import Dashboard
from components.add_expense import AddExpense
from components.reports import Reports
from components.profile import Profile
from components.auth import Auth

class MyExpensesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Expenses")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ffffff")
        
        # Color scheme
        self.colors = {
            "primary": "#4CAF50",  # Green
            "secondary": "#2196F3", # Blue
            "background": "#ffffff", # White
            "text": "#333333"
        }
        
        # Initialize authentication
        self.auth = Auth(self)
        self.current_user = None
        
        # Create menu button
        self.menu_button = tk.Button(
            self.root, 
            text="☰", 
            font=("Arial", 20), 
            bg=self.colors["primary"],
            fg="white",
            borderwidth=0,
            command=self.show_menu
        )
        self.menu_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)
        
        # Menu frame (initially hidden)
        self.menu_frame = tk.Frame(
            self.root, 
            bg=self.colors["secondary"],
            width=200,
            height=600,
            bd=2,
            relief=tk.RAISED
        )
        
        # Menu items
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Add Expense", self.show_add_expense),
            ("Generate Report", self.show_reports),
            ("Profile", self.show_profile),
            ("Logout", self.logout)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                font=("Arial", 12),
                bg=self.colors["secondary"],
                fg="white",
                borderwidth=0,
                anchor=tk.W,
                command=command
            )
            btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Main content frame
        self.content_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize pages
        self.pages = {
            "dashboard": Dashboard(self.content_frame, self),
            "add_expense": AddExpense(self.content_frame, self),
            "reports": Reports(self.content_frame, self),
            "profile": Profile(self.content_frame, self)
        }
        
        # Hide all pages initially
        for page in self.pages.values():
            page.pack_forget()
        
        # Show login dialog first
        self.auth.show_login()
    
    def show_menu(self):
        # Toggle menu visibility
        if self.menu_frame.winfo_ismapped():
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.content_frame)
    
    def show_dashboard(self):
        self.hide_all_pages()
        self.pages["dashboard"].pack(fill=tk.BOTH, expand=True)
        self.pages["dashboard"].refresh()
        self.menu_frame.pack_forget()
    
    def show_add_expense(self):
        self.hide_all_pages()
        self.pages["add_expense"].pack(fill=tk.BOTH, expand=True)
        self.menu_frame.pack_forget()
    
    def show_reports(self):
        self.hide_all_pages()
        self.pages["reports"].pack(fill=tk.BOTH, expand=True)
        self.pages["reports"].generate_reports()
        self.menu_frame.pack_forget()
    
    def show_profile(self):
        self.hide_all_pages()
        self.pages["profile"].pack(fill=tk.BOTH, expand=True)
        self.menu_frame.pack_forget()
    
    def hide_all_pages(self):
        for page in self.pages.values():
            page.pack_forget()
    
    def logout(self):
        self.current_user = None
        self.hide_all_pages()
        self.auth.show_login()
        self.menu_frame.pack_forget()
    
    def on_login_success(self, user):
        self.current_user = user
        self.show_dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyExpensesApp(root)
    root.mainloop()