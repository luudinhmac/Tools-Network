# Cách sử dụng 

![alt](https://github.com/luudinhmac/Tools-Network/blob/master/syslog/image.png)

`Mặc định syslog dùng port 514`
`Có thể thay đổi port trong router`
```sh
Trong router cấu hình như sau
logging trap debugging
logging host 192.168.37.1 transport udp port 1514
```sh

`Vào trang login.live.com để tạo 1 mail outlook`
Ngoài ra , bạn tạo 1 file text tên là send_mail_alarm.txt , ở cùng thư mục chứa tool. Nội dung file này là điền các từ khóa xuất hiện trong message cần gửi mail
VD
```sh
administratively-down
OSPF-down
```sh
