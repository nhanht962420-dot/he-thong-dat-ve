import socket
import threading

# Cấu hình Server
HOST = '127.0.0.1'
PORT = 65432

# Dữ liệu ghế: ID -> Trạng thái (True: Trống, False: Đã đặt)
seats = {i: True for i in range(1, 11)}
# Lock để đảm bảo tính đồng bộ (Thread-safe)
seat_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            # Gửi danh sách ghế hiện tại cho Client
            current_status = str(seats)
            conn.sendall(current_status.encode('utf-8'))
            
            # Nhận yêu cầu đặt ghế (ID ghế)
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            
            seat_id = int(data)
            response = ""

            # Khu vực kiểm tra và đặt ghế (Sử dụng Lock)
            with seat_lock:
                if seat_id in seats and seats[seat_id]:
                    seats[seat_id] = False
                    response = "SUCCESS: Bạn đã đặt ghế số {} thành công!".format(seat_id)
                else:
                    response = "FAILED: Ghế đã có người đặt hoặc không tồn tại."
            
            conn.sendall(response.encode('utf-8'))
    except:
        pass
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()