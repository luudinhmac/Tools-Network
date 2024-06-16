import re
import datetime
import calendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import netmiko

############SEND MAIL FUNCTION###############
def sendMail(output, dstMail):
    if output != '':
        msg = MIMEMultipart()
        msg['From'] = 'luumac2801@gmail.com'
        msg['To'] = dstMail
        msg['Subject'] = "WARNING!!!  -> Someone logs into the device!"
        msg.attach(MIMEText(output, 'plain'))
        text = msg.as_string()
        s = smtplib.SMTP(host='smtp-mail.outlook.com')
        s.starttls()
        s.login('luumac2801@gmail.com', 'password')
        s.sendmail("luumac2801@gmail.com", dstMail, text)
        s.quit()

#######################################
sw1 = {
    'device_type': 'cisco_ios',
    'ip': '10.1.2.3',
    'username': 'monitor',
    'password': 'abc@123',
    'secret': 'abc@123',
    'verbose': False,
}

# Establish SSH connection to Cisco switch
net_connect = netmiko.ConnectHandler(**sw1)
net_connect.enable()

# Retrieve command output from the switch
get_time1 = net_connect.send_command_timing('show logging | inc LOGIN-5-LOGIN_SUCCESS')

# Process the output directly
lines = get_time1.splitlines()
for line in lines:
    # Extract time and date from the log line
    time_log = re.findall(r'(?:at) (\d\d:\d\d:\d\d).*(\w\w\w \w\w\w \d\d \d\d\d\d)', line)
    user_login = re.findall(r'user:(\w+)', line)
    
    for time1 in time_log:
        hour, minute, second = time1[0].split(":")
        day, month_abbr, year = time1[1].split()
        mon_number = list(calendar.month_abbr).index(month_abbr) # Convert month abbreviation to number
        
        # Calculate time difference
        login_time = datetime.datetime(int(year), mon_number, int(day), int(hour), int(minute), int(second))
        current_time = datetime.datetime.now()
        delta_time = current_time - login_time
        
        # Check if login occurred within the last 5 minutes
        if delta_time.total_seconds() <= 300:
            output = f"New login found: {user_login}"
            sendMail(output, "luumac2801@gmail.com")

# Disconnect from SSH session
net_connect.disconnect()
