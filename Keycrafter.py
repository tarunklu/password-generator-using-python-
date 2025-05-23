import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

# ------------------ Main Window Setup ------------------
root = tk.Tk()
root.title("KeyCrafter - Password Generator")
root.geometry("700x550")
root.config(bg="#000000")

previous_passwords = []

# ------------------ Password Generator Logic ------------------
def generate_password():
    length = password_length.get()
    use_upper = var_upper.get()
    use_numbers = var_numbers.get()
    use_special = var_special.get()

    char_pool = string.ascii_lowercase
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_numbers:
        char_pool += string.digits
    if use_special:
        char_pool += string.punctuation

    if not char_pool:
        messagebox.showwarning("Selection Missing", "Please select at least one character type.")
        return

    password = ''.join(random.choice(char_pool) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    previous_passwords.insert(0, password)
    update_history()
    update_security_rating(length, use_upper, use_numbers, use_special)

# ------------------ Copying Functions ------------------
def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def copy_specific(p):
    pyperclip.copy(p)
    messagebox.showinfo("Copied", f"Copied:\n{p}")

# ------------------ Update Password History ------------------
def update_history():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for pw in previous_passwords[:7]:
        row_frame = tk.Frame(scrollable_frame, bg="#1a1a1a")
        row_frame.pack(fill="x", pady=2, padx=5)

        pw_label = tk.Label(row_frame, text=pw, anchor="w", font=("Courier", 10), width=45, bg="#1a1a1a", fg="white")
        pw_label.pack(side="left", padx=5)

        copy_btn = ttk.Button(row_frame, text="Copy", width=8, command=lambda p=pw: copy_specific(p))
        copy_btn.pack(side="right", padx=5)

# ------------------ Password Security Rating ------------------
def update_security_rating(length, upper, number, special):
    strength = sum([length >= 12, upper, number, special])
    if strength >= 4 and length >= 16:
        security_label.config(text="Security: HIGH", fg="green")
    elif strength >= 3:
        security_label.config(text="Security: MEDIUM", fg="orange")
    else:
        security_label.config(text="Security: LOW", fg="red")

# ------------------ Clear Function ------------------
def clear_password():
    password_entry.delete(0, tk.END)
    security_label.config(text="Security: UNKNOWN", fg="white")

# ------------------ UI Layout ------------------

# Title
tk.Label(root, text="KeyCrafter", font=("Helvetica", 18, "bold"), bg="#000000", fg="white").pack(pady=10)
tk.Label(root, text="Create Powerful and One-of-a-Kind Passwords", bg="#000000", fg="white").pack()

# Controls Frame
frame = tk.Frame(root, bg="#000000")
frame.pack(pady=10)

# Length Slider
tk.Label(frame, text="Choose Password Length:", bg="#000000", fg="white").grid(row=0, column=0, sticky="w")
password_length = tk.IntVar(value=12)
tk.Scale(frame, from_=8, to=24, orient=tk.HORIZONTAL, variable=password_length, length=200,
         bg="#000000", fg="white", highlightbackground="#000000").grid(row=0, column=1)

# Checkboxes
var_upper = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)

tk.Checkbutton(frame, text="Capital Letters", variable=var_upper, bg="#000000", fg="white").grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame, text="Numbers", variable=var_numbers, bg="#000000", fg="white").grid(row=2, column=0, sticky="w")
tk.Checkbutton(frame, text="Special Characters", variable=var_special, bg="#000000", fg="white").grid(row=3, column=0, sticky="w")
tk.Checkbutton(frame, text= "Lower Letters", variable=var_lower, bg="#000000", fg="white").grid(row=4, column=0, sticky="w")
# Password Entry
password_entry = ttk.Entry(root, font=("Courier", 16), width=40)
password_entry.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#000000")
btn_frame.pack()
ttk.Button(btn_frame, text="Generate", command=generate_password).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Copy to Clipboard", command=copy_password).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Clear", command=clear_password).grid(row=0, column=2, padx=10)

# Security Label
security_label = tk.Label(root, text="Security: UNKNOWN", font=("Helvetica", 12), bg="#000000", fg="white")
security_label.pack(pady=5)

# History Section
tk.Label(root, text="Previously Generated Keys", bg="#000000", fg="white").pack()

# Scrollable Frame for History
history_container = tk.Frame(root)
history_container.pack(pady=5, fill="x", expand=True)

canvas = tk.Canvas(history_container, bg="#000000", highlightthickness=0, height=120)
scrollbar = ttk.Scrollbar(history_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#000000")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="right", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Footer
tk.Label(root, text="For Contact: dowork016@gmail.com", font=("Arial", 8), bg="#000000", fg="white").pack(pady=10)

# Run App
root.mainloop()
