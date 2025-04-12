import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Profile:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=self.app.colors["background"])
        
        # Title
        self.title = tk.Label(
            self.frame,
            text="User Profile",
            font=("Arial", 20, "bold"),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        )
        self.title.pack(pady=20)
        
        # Profile info frame
        info_frame = tk.Frame(self.frame, bg=self.app.colors["background"])
        info_frame.pack(pady=10)
        
        # Username
        tk.Label(
            info_frame,
            text="Username:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        
        self.username_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        )
        self.username_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Email
        tk.Label(
            info_frame,
            text="Email:",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        ).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.email_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 12),
            bg=self.app.colors["background"],
            fg=self.app.colors["text"]
        )
        self.email_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Change password button
        change_pass_btn = tk.Button(
            self.frame,
            text="Change Password",
            font=("Arial", 12),
            bg=self.app.colors["secondary"],
            fg="white",
            command=self.show_change_password
        )
        change_pass_btn.pack(pady=20)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self.load_profile()
    
    def pack_forget(self):
        self.frame.pack_forget()
    
    def load_profile(self):
        if self.app.current_user:
            self.username_label.config(text=self.app.current_user["username"])
            self.email_label.config(text=self.app.current_user["email"])
    
    def show_change_password(self):
        # Create popup window
        popup = tk.Toplevel(self.parent)
        popup.title("Change Password")
        popup.geometry("400x300")
        popup.resizable(False, False)
        
        # Current password
        tk.Label(
            popup,
            text="Current Password:",
            font=("Arial", 12)
        ).pack(pady=(20, 5))
        
        self.current_pass_entry = tk.Entry(popup, show="*", font=("Arial", 12))
        self.current_pass_entry.pack(pady=5)
        
        # New password
        tk.Label(
            popup,
            text="New Password:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.new_pass_entry = tk.Entry(popup, show="*", font=("Arial", 12))
        self.new_pass_entry.pack(pady=5)
        
        # Confirm new password
        tk.Label(
            popup,
            text="Confirm New Password:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        self.confirm_pass_entry = tk.Entry(popup, show="*", font=("Arial", 12))
        self.confirm_pass_entry.pack(pady=5)
        
        # Submit button
        submit_btn = tk.Button(
            popup,
            text="Change Password",
            font=("Arial", 12),
            bg=self.app.colors["primary"],
            fg="white",
            command=lambda: self.change_password(popup)
        )
        submit_btn.pack(pady=20)
    
    def change_password(self, popup):
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        # Validate
        if not current_pass or not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords don't match")
            return
        
        if len(new_pass) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Verify current password
        conn = sqlite3.connect("data/expenses.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT password FROM users WHERE id = ?
            """, (self.app.current_user["id"],))
            
            result = cursor.fetchone()
            if not result or result[0] != current_pass:  # In real app, use hashed passwords
                messagebox.showerror("Error", "Current password is incorrect")
                return
            
            # Update password
            cursor.execute("""
                UPDATE users SET password = ? WHERE id = ?
            """, (new_pass, self.app.current_user["id"]))
            
            conn.commit()
            messagebox.showinfo("Success", "Password changed successfully")
            popup.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")
        finally:
            conn.close()