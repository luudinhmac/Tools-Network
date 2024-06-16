import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import socket
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import webbrowser

def open_help_url():
    webbrowser.open('https://github.com/luudinhmac/Tools-Network')


def start_syslog_server():
    # Get values from the entries
    ip_listen = ip_entry.get()
    udp_port = port_entry.get()
    sender_email = email_entry.get()
    password = password_entry.get()  # Be cautious with password handling
    recipient_email = recipient_email_entry.get()
    
    # Here you should add the code to start the syslog server
    # and setup the logic for sending an email if the message contains the keyword
    # For now, we just display a message
    messagebox.showinfo("Info", f"Starting syslog server on {ip_listen}:{udp_port}\n"
                                f"Email will be sent from: {sender_email}\n"
                                f"Email will be sent to: {recipient_email}")
                                
        # Starting the syslog server in a separate thread
    threading.Thread(target=listen_for_syslog_messages, args=(ip_listen, udp_port)).start()
    #messagebox.showinfo("Info", f"Syslog server is starting on {ip_listen}:{udp_port}\nMonitoring for keyword: '{msg_keyword}'")




    
def sendMail(output,mail_sender,mail_receive,password):
 if(output!=''):
  msg = MIMEMultipart()
  msg['From'] = mail_sender
  msg['To'] = mail_receive
  msg['Subject'] = "#####NETWORK ALARM####"
  msg.attach(MIMEText(output, 'plain'))
  text=msg.as_string()


  s = smtplib.SMTP(host='smtp-mail.outlook.com',port='587')
  s.starttls()
  s.login(mail_sender, password)


  s.sendmail(mail_sender,mail_receive,text)


  s.quit()





def read_keywords_from_config(file_path):
    with open(file_path, 'r') as file:
        # Đọc mỗi dòng và chia từ khóa bằng dấu gạch ngang (-)
        keywords = [line.strip().lower() for line in file]
    return keywords

        
def listen_for_syslog_messages(ip, port):

    sender_email = email_entry.get()
    password = password_entry.get()  # Be cautious with password handling
    recipient_email = recipient_email_entry.get()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, int(port)))
    config_path='send_mail_alarm.txt' ##cùng folder với file script
    # Đọc danh sách từ khóa từ file config
    keyword_groups = read_keywords_from_config(config_path)
    print(f"Syslog server is listening on {ip}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        message = data.decode('utf-8').lower()
        ip_source=addr[0]
        #print(f"Received message: {message}")

        # Kiểm tra từng nhóm từ khóa
        for keywords in keyword_groups:
            # Kiểm tra nếu tất cả từ khóa trong nhóm đều có trong message
            if all(keyword.strip() in message for keyword in keywords.split('-')):
                print("Detect event need to send alarm")
                msg_sent=ip_source+"----"+message
                sendMail(msg_sent,sender_email,recipient_email,password)
                # Tại đây có thể gửi email hoặc thực hiện hành động khác
                #break  # Nếu đã tìm thấy một nhóm từ khóa, không cần kiểm tra các nhóm khác
                
                
                
                
# Create the main window
root = tk.Tk()
root.title("SIMPLE SYSLOG SERVER")
icon = PhotoImage(file='iconmail.ico')
# Set the icon of the window
root.iconphoto(True, icon)

root.geometry("400x230")
# Create and place the IP entry
ip_label = tk.Label(root, text="IP Server Syslog")
ip_label.grid(row=0, column=0, sticky="e", padx=5, pady=(10, 2))
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=(10, 2))

# Create and place the port entry
port_label = tk.Label(root, text="Listen on UDP")
port_label.grid(row=1, column=0, sticky="e", padx=5, pady=2)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

# Create and place the keyword entry
'''keyword_label = tk.Label(root, text="Msg send mail")
keyword_label.grid(row=2, column=0, sticky="e", padx=5, pady=2)
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)'''

# Create and place the sender email entry
email_label = tk.Label(root, text="Email(Outlook) gửi")
email_label.grid(row=3, column=0, sticky="e", padx=5, pady=2)
email_entry = tk.Entry(root)
email_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

# Create and place the password entry
password_label = tk.Label(root, text="Password")
password_label.grid(row=4, column=0, sticky="e", padx=5, pady=2)
password_entry = tk.Entry(root, show="*")  # Use show="*" for password masking
password_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

# Create and place the recipient email entry
recipient_email_label = tk.Label(root, text="Email nhận")
recipient_email_label.grid(row=5, column=0, sticky="e", padx=5, pady=2)
recipient_email_entry = tk.Entry(root)
recipient_email_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

# Create and place the start button
start_button = tk.Button(root, text="START", command=start_syslog_server,bg='light blue')
start_button.grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 10))

# Set the column configuration for proper expansion
root.grid_columnconfigure(1, weight=1)

help_label = tk.Label(root, text="How to use", fg="blue", cursor="hand2")
help_label.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 0))
help_label.bind("<Button-1>", lambda e: open_help_url())

# Run the main loop
root.mainloop()
