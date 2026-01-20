import socket

HOST = '127.0.0.1'
PORT = 65432

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            # Nhận danh sách ghế từ Server
            data = s.recv(1024).decode('utf-8')
            print(f"\nDanh sách ghế (True = Trống): \n{data}")
            
            choice = input("Nhập số ghế muốn đặt (hoặc 'q' để thoát): ")
            if choice.lower() == 'q':
                break
            
            s.sendall(choice.encode('utf-8'))
            
            # Nhận kết quả phản hồi
            result = s.recv(1024).decode('utf-8')
            print(f"-> Kết quả: {result}")

if __name__ == "__main__":
    start_client()