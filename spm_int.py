import tkinter as tk
import hashlib
from tkinter import simpledialog, messagebox
from db_man import get_pass, get_mpass, add_mpass, add_pass
from encryptor import pass_encypt, pass_decrypt, key_gen, key_read
import sys

def mpass_dialog():
    stored_mpass = get_mpass()
    stored_mpass = stored_mpass.decode('utf-8')
    if stored_mpass is None:
        new_mpass = simpledialog.askstring("Set Master Password","Create New Master Password:", show="*")
        if new_mpass:
            add_mpass(new_mpass)
            messagebox.showinfo("Success","Master Password Create Successfully!")
    else:
        trys = 3
        while trys > 0:
            enter_mpass = simpledialog.askstring("SPM Authentication","Enter Your Master Password:", show="*")
            if enter_mpass is None:
                break
            entered_hashmpass = hashlib.sha256(enter_mpass.encode("utf-8")).hexdigest()
            entered_hashmpass = entered_hashmpass
            if entered_hashmpass == stored_mpass:
                messagebox.showinfo("Access Granted!", "Welcome!")
                break
            else:
                trys -= 1
                messagebox.showerror("Ivalid", f"Entered Password is Incorrect \nPlease try again!\nAttempts Left: {trys}")
        if trys == 0:
            messagebox.showerror("Access Denied!", "Too many Incorrect attempts")
            sys.exit()


def addpass_ui():
    root = tk.Tk()
    root.title("Simple Password Manager")
    favicon = tk.PhotoImage(file='spm_logo.png')
    root.iconphoto(True,favicon)
    def save_pass():
        account = account_entry.get()
        password = password_entry.get()
        username = username_entry.get()
        encrypted_pass = pass_encypt(password)
        add_pass(account, username, encrypted_pass)
        status_label.config(text="Password is saved securely!")
    
    def view_pass():
        password = get_pass()
        view_window = tk.Toplevel(root)
        view_window.title("Stored Passwords")

        for idx, (account, username, encypted_pass) in enumerate(password):
            decrypted_pass = pass_decrypt(encypted_pass)
            tk.Label(text=f"Account : {account}").grid(row=idx*3, column=0)
            tk.Label(text=f"UserName : {username}").grid(row=idx*3+1, column=0)
            tk.Label(text=f"Password : {decrypted_pass}").grid(row=idx*3+2,column=0)
    
    tk.Label(root, text="Account").grid(row=0)
    tk.Label(root, text="Username").grid(row=1)
    tk.Label(root, text="Password").grid(row=2)

    account_entry = tk.Entry(root)
    username_entry = tk.Entry(root)
    password_entry = tk.Entry(root)

    account_entry.grid(row=0, column=1)
    username_entry.grid(row=1, column=1)
    password_entry.grid(row=2, column=1)

    save_btn = tk.Button(root, text="Save", command=save_pass)
    save_btn.grid(row=3, column=1)

    view_label = tk.Label(root, text="To View Stored Passwords Click!")
    view_btn = tk.Button(root, text="View", command=view_pass)
    view_label.grid(row=4,column=1)
    view_btn.grid(row=4, column=2)

    status_label = tk.Label(root, text="")
    status_label.grid(row=5, column=1)

    root.mainloop()

if __name__ == "__main__":
    mpass_dialog()
    addpass_ui()






