from netmiko import ConnectHandler

import re

#khai báo các switch

sw_user2={

                        'device_type': 'cisco_ios',

                        'ip': '192.168.64.100',

                        'username': 'admin',

                        'password': 'abc@1234',

                        'secret': 'abc@1234',

                        'verbose': False,

}

 

sw_user3={

                        'device_type': 'cisco_ios',

                        'ip': '192.168.64.101',

                        'username': 'admin',

                        'password': 'abc@1234',

                        'secret': 'abc@1234',

                        'verbose': False,

}

 

sw_user4={

                        'device_type': 'cisco_ios',

                        'ip': '192.168.64.102',

                        'username': 'admin',

                        'password': 'abc@1234',

                        'secret': 'abc@1234',

                        'verbose': False,

}

 

#------------------------Login vào switch-----------------------#

all_switches=[sw_user2,sw_user3,sw_user4]

for switches in all_switches:

 net_connect=ConnectHandler(**switches)

 net_connect.enable()

 print('\n\n********************shut and no shut cac port tren '+ switches['ip'] +'******************')

 wr=net_connect.send_command_timing("show mac address-table | include (c074|000b)") ##MÁC CỦA IP PHONE HÃNG GRANDSTREAM

 f=open('temp.txt','w') ##Ghi mac vào file tạm

 f.write(wr)

 f.close()

 f=open('temp.txt','r') ##Mở file tạm ra

 linehai=f.readlines()

 for i in range (0,len(linehai)):

  if ('Gi' in linehai[i]):

   port=re.findall(r'Gi.*',linehai[i])[0] ##Lấy port tương ứng với MAC

   command= "int "+port+" \n shut \n no shut \n" ##Lệnh shutdown, no shutdown

   print(command)

   net_connect.send_command_timing('conf t')

   net_connect.send_command_timing(command) ##Thực hiện lệnh ở trên
   