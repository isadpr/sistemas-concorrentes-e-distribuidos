import socket
import time
import threading
import random
import datetime
import time

def client_process(process_id, r):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5001)) 
    for _ in range(r):
        s.sendall(f"REQUEST|{process_id}".encode())
        
        response = s.recv(1024).decode()
        if response.startswith("GRANT"): 

            with open("resultado.txt", "a") as f:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                f.write(f"{timestamp} | {process_id}\n")

            time.sleep(random.randint(1, 10)) 
            s.sendall(f"RELEASE|{process_id}".encode())
        else:
            print(f"Processo {process_id} não recebeu GRANT, tentando novamente...")

        time.sleep(random.randint(1, 10)) 

    s.close()

threads = []
for i in range(5):
    t = threading.Thread(target=client_process, args=(i, 1))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
