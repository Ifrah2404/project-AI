import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Auth:
    def __init__(self, app):
        self.app = app
        self.login_window = None
        self.register_window = None
    
    def show_login(self):
        # Create login window
        self.login_window = tk.Toplevel(self.app.root)
        self.login_window.title("Login")
        self.login_window.geometry("400x300")
        self.login_window.resizable(False, False)
        
        # Center the window
        window_width = 400
        window_height = 300
        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Login form
        tk.Label(
            self.login_window,
            text="Login to My Expenses",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Username
        tk.Label(
            self.login_window,
            text="Username:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.username_entry = tk.Entry(self.login_window, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(
            self.login_window,
            text="Password:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.password_entry = tk.Entry(self.login_window, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        
        # Login button
        login_btn = tk.Button(
            self.login_window,
            text="Login",
            font=("Arial", 12),
            bg=self.app.colors["primary"],
            fg="white",
            command=self.login
        )
        login_btn.pack(pady=20)
        
        # Register link
        tk.Label(
            self.login_window,
            text="Don't have an account?",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=20)
        
        register_link = tk.Label(
            self.login_window,
            text="Register",
            font=("Arial", 10, "underline"),
            fg="blue",
            cursor="hand2"
        )
        register_link.pack(side=tk.LEFT)
        register_link.bind("<Button-1>", lambda e: self.show_register())
        
        # Make the login window modal
        self.login_window.grab_set()
        self.login_window.transient(self.app.root)
    
    def show_register(self):
        if self.login_window:
            self.login_window.destroy()
        
        # Create register window
        self.register_window = tk.Toplevel(self.app.root)
        self.register_window.title("Register")
        self.register_window.geometry("400x400")
        self.register_window.resizable(False, False)
        
        # Center the window
        window_width = 400
        window_height = 400
        screen_width = self.register_window.winfo_screenwidth()
        screen_height = self.register_window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.register_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Register form
        tk.Label(
            self.register_window,
            text="Create a New Account",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Username
        tk.Label(
            self.register_window,
            text="Username:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.reg_username_entry = tk.Entry(self.register_window, font=("Arial", 12))
        self.reg_username_entry.pack(pady=5)
        
        # Email
        tk.Label(
            self.register_window,
            text="Email:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.reg_email_entry = tk.Entry(self.register_window, font=("Arial", 12))
        self.reg_email_entry.pack(pady=5)
        
        # Password
        tk.Label(
            self.register_window,
            text="Password:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.reg_password_entry = tk.Entry(self.register_window, show="*", font=("Arial", 12))
        self.reg_password_entry.pack(pady=5)
        
        # Confirm Password
        tk.Label(
            self.register_window,
            text="Confirm Password:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.reg_confirm_entry = tk.Entry(self.register_window, show="*", font=("Arial", 12))
        self.reg_confirm_entry.pack(pady=5)
        
        # Register button
        register_btn = tk.Button(
            self.register_window,
            text="Register",
            font=("Arial", 12),
            bg=self.app.colors["primary"],
            fg="white",
            command=self.register
        )
        register_btn.pack(pady=20)
        
        # Login link
        tk.Label(
            self.register_window,
            text="Already have an account?",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=20)
        
        login_link = tk.Label(
            self.register_window,
            text="Login",
            font=("Arial", 10, "underline"),
            fg="blue",
            cursor="hand2"
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind("<Button-1>", lambda e: self.show_login())
        
        # Make the register window modal
        self.register_window.grab_set()
        self.register_window.transient(self.app.root)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        conn = sqlite3.connect("data/expenses.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, username, email FROM users 
                WHERE username = ? AND password = ?
            """, (username, password))  # In real app, use password hashing
            
            user = cursor.fetchone()
            
            if user:
                self.app.on_login_success({
                    "id": user[0],
                    "username": user[1],
                    "email": user[2]
                })
                self.login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
        finally:
            conn.close()
    
    def register(self):
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        if not username or not email or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        conn = sqlite3.connect("data/expenses.db")
        cursor = conn.cursor()
        
        try:
            # Check if username exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return
            
            # Create new user
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, password))
            
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully")
            self.show_login()
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
        finally:
            conn.close()