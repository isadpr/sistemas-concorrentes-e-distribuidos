import socket
import threading
from queue import Queue
import time
import sys

class Coordinator:
    def __init__(self):
        self.request_queue = Queue() 
        self.access_count = {}
        self.lock = threading.Lock()
        self.connections = {}
        self.current_process = None
        self.running = True
        self.process_status = {}  

    def log_mensagem(self, tipo, id_process):
        mensagem = self.format_message(tipo, id_process)
        
        timestamp = time.time()
        formatted_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        log_entry = f"{formatted_timestamp} | {mensagem}\n"
        
        with open("log.txt", "a") as log_file:
            log_file.write(log_entry)

    def format_message(self, msg_type, process_id):
        message = f"{msg_type}|{process_id}|000000"
        return message[:10]

    def handle_client(self, conn, addr):
        process_id = None
        while True:
            data = conn.recv(1024).decode()
            if not data:
                if process_id:
                    del self.connections[process_id]
                break

            msg_type, process_id, _ = data.split('|')

            if process_id in self.process_status and self.process_status[process_id] == 'completed':
                continue

            if msg_type == '1':
                with self.lock:
                    self.request_queue.put(process_id) 
                    self.connections[process_id] = conn
                    self.log_mensagem('1', process_id) 
                    self.send_grant()

            elif msg_type == '3':
                with self.lock:
                    self.access_count[process_id] = self.access_count.get(process_id, 0) + 1
                    self.current_process = None
                    self.process_status[process_id] = 'completed'
                    self.log_mensagem('3', process_id) 
                    self.send_grant()

    def send_grant(self):
        if self.current_process is None and not self.request_queue.empty():
            next_process = self.request_queue.get()
            self.current_process = next_process
            grant_message = self.format_message(2, next_process)
            conn = self.connections.get(next_process)
            if conn:
                conn.send(grant_message.encode())
                self.log_mensagem('2', next_process)

    def start_terminal_interface(self):
        while self.running:
            print("\nComandos disponíveis:")
            print("1 - Imprimir fila de pedidos")
            print("2 - Imprimir quantas vezes cada processo foi atendido")
            print("3 - Encerrar execução")
            comando = input("Digite o número do comando: ")

            if comando == "1":
                self.print_request_queue()
            elif comando == "2":
                self.print_access_count()
            elif comando == "3":
                self.running = False
                print("Encerrando execução...")
                sys.exit()
            else:
                print("Comando inválido!")

    def print_request_queue(self):
        print("\nFila de Pedidos:")
        if self.request_queue.empty():
            print("Nenhum pedido na fila.")
        else:
            for item in list(self.request_queue.queue):
                print(f"Processo {item}")

    def print_access_count(self):
        print("\nAtendimentos por Processo:")
        if not self.access_count:
            print("Nenhum processo foi atendido ainda.")
        else:
            for id_process, count in self.access_count.items():
                print(f"Processo {id_process}: {count} vez(es)")

def start_server(coordinator):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5001))
    server_socket.listen(5)
    
    while coordinator.running:
        conn, addr = server_socket.accept()
        threading.Thread(target=coordinator.handle_client, args=(conn, addr)).start()

    server_socket.close()

coordinator = Coordinator()

server_thread = threading.Thread(target=start_server, args=(coordinator,))
terminal_thread = threading.Thread(target=coordinator.start_terminal_interface)

server_thread.start()
terminal_thread.start()

terminal_thread.join()

coordinator.running = False
server_thread.join()