import ftplib
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

class FTPUploaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FTP Uploader")

        # FTP Server Address
        tk.Label(master, text="FTP Server Address:").grid(row=0, column=0, sticky="w")
        self.server_entry = tk.Entry(master)
        self.server_entry.grid(row=0, column=1, padx=10, pady=5)
        self.server_entry.focus_set()  # Set focus to server entry

        # Username
        tk.Label(master, text="Username:").grid(row=1, column=0, sticky="w")
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password
        tk.Label(master, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.password_entry.bind("<Return>", lambda event: self.upload_file())  # Bind Enter key to upload function

        # Local File Path
        tk.Label(master, text="Local File Path:").grid(row=3, column=0, sticky="w")
        self.file_path_entry = tk.Entry(master)
        self.file_path_entry.grid(row=3, column=1, padx=10, pady=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=3, column=2, padx=10, pady=5)

        # Upload Button
        self.upload_button = tk.Button(master, text="Upload", command=self.upload_file)
        self.upload_button.grid(row=4, columnspan=2, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def upload_file(self):
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        local_file_path = self.file_path_entry.get()

        if not local_file_path:
            messagebox.showwarning("Warning", "Please select file or folder.")
            return

        try:
            # Connect to FTP server
            ftp = ftplib.FTP(server)
            ftp.login(username, password)

            # Get the current date and time
            now = datetime.datetime.now()
            date_string = now.strftime("%Y-%m-%d")
            folder_name = date_string

            # Create directory if not exists
            try:
                ftp.mkd(folder_name)
                messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.\nPath: {ftp.pwd()}/{folder_name}")
            except ftplib.error_perm as e:
                messagebox.showwarning("Warning", f"Directory {folder_name} already exists or cannot be created: {e}")

            # Change to the new folder
            ftp.cwd(folder_name)

            # Upload a file to the new folder
            file_name = os.path.basename(local_file_path)
            with open(local_file_path, 'rb') as f:
                ftp.storbinary('STOR ' + file_name, f)

            # Inform user about successful upload
            messagebox.showinfo("Upload Successful", f"File '{file_name}' uploaded successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Close the FTP connection
            if 'ftp' in locals() and ftp:
                ftp.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPUploaderApp(root)
    root.mainloop()
