import socket
import time
import threading
import random

def client_process(process_id, r):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5001)) 
    for _ in range(r):
        s.sendall(f"1|{process_id}|000000".encode())
        
        response = s.recv(1024).decode()
        if response.startswith("2"): 
            time.sleep(random.randint(1, 10)) 
            s.sendall(f"3|{process_id}|000000".encode())
        else:
            print(f"Processo {process_id} não recebeu GRANT, tentando novamente...")

    s.close()

threads = []
for i in range(5):
    t = threading.Thread(target=client_process, args=(i, 2))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
