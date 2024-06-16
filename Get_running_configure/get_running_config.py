import tkinter as tk
import webbrowser
import netmiko

def get_config():
    router_ips = text_box.get('1.0', 'end-1c').split('\n')
    username = username_entry.get()
    password = password_entry.get()
    
    for ip in router_ips:
        if not ip.strip():
            continue
        
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
            'secret': password,  # Assuming secret is the same as password
            'verbose': False,
        }
        
        try:
            net_connect = netmiko.ConnectHandler(**device)
            net_connect.enable()
            get_cfg = net_connect.send_command_timing('show run')
            
            # Write to file
            with open(f"{ip}_cfg.txt", 'w') as f:
                f.write(get_cfg)
            
            status_label.config(text=f"DONE BACKUP FOR {ip}")
            root.update()
            
            # Clear status after 2 seconds
            root.after(2000, lambda: status_label.config(text=""))
            
        except Exception as e:
            status_label.config(text=f"ERROR: {str(e)}")
            root.update()
            continue

def open_webpage(event):
    webbrowser.open_new(r"https://github.com/luudinhmac/Tools-Network/tree/master/Get_running_configure")

# Create the tkinter window
root = tk.Tk()
root.title("Network Config Backup Tool")

# Widgets
label = tk.Label(root, text="Get running config", font=("Helvetica", 14))
label.pack()

text_box = tk.Text(root, height=5, width=30)
text_box.pack()

username_label = tk.Label(root, text="Username")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

button = tk.Button(root, text="GET CONFIG", command=get_config, bg='#40E0D0')
button.pack(pady=(10, 0))

status_label = tk.Label(root, text="")
status_label.pack()

link = tk.Label(root, text="XEM SOURCE CỦA TOOL", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", open_webpage)

root.geometry("500x400")
root.mainloop()
