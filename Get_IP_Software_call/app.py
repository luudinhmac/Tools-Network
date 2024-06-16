import psutil ##Cần cài module theo lệnh pip install psutil
import socket
import time

process_name = input("Nhập name of process, ví dụ zalo.exe: ")
print("\n")

def find_process_connections(process_name):
    connections = []
    for proc in psutil.process_iter(['name', 'connections']):
        if proc.info['name'] == process_name:
            for conn in proc.info['connections']:
                if conn.laddr and conn.raddr and socket.AF_INET == conn.family:
                    connections.append({
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_addr': f"{conn.raddr.ip}",
                    })
    return connections

def monitor_process_connections(process_name, interval=5):
    """Liên tục theo dõi và in ra các kết nối của tiến trình.
    
    Args:
        process_name (str): Tên của quá trình cần theo dõi.
        interval (int, optional): Khoảng thời gian giữa mỗi lần kiểm tra, tính bằng giây. Mặc định là 5 giây.
    """


    print(f"Monitoring connections for {process_name}. Press Ctrl+C to stop.\n\n")
    try:
        while True:
            connections = find_process_connections(process_name)
            if connections:  # Kiểm tra xem có kết nối nào không
                for conn in connections:
                    print(f"{conn['remote_addr']}")
            else:
                print("No connections found.")
            
            time.sleep(interval)  # Đợi một khoảng thời gian trước khi kiểm tra lại
    except KeyboardInterrupt:
        print("Monitoring stopped.")

monitor_process_connections(process_name)