import threading
import time
import random
from queue import Queue

BUFFER_SIZE = 5
SIMULATION_TIME = 10

class BufferMonitor:
    def __init__(self, size):
        self.buffer = Queue(size)
        self.lock = threading.Condition()
        self.size = size
        
    def produce(self, item, producer_id):
        with self.lock:
            while self.buffer.full():
                print(f"Produtor {producer_id} esperando - buffer cheio")
                self.lock.wait()
                
            self.buffer.put(item)
            print(f"Produtor {producer_id} produziu: {item} | Buffer: {list(self.buffer.queue)}")
            self.lock.notify_all()
    
    def consume(self, consumer_id):
        with self.lock:
            while self.buffer.empty():
                print(f"Consumidor {consumer_id} esperando - buffer vazio")
                self.lock.wait()
                
            item = self.buffer.get()
            print(f"Consumidor {consumer_id} consumiu: {item} | Buffer: {list(self.buffer.queue)}")
            self.lock.notify_all()
            return item

def producer(monitor, id):
    while True:
        item = random.randint(1, 100)
        time.sleep(random.uniform(0.1, 0.5))
        monitor.produce(item, id)

def consumer(monitor, id):
    while True:
        time.sleep(random.uniform(0.1, 0.8))
        item = monitor.consume(id)
        time.sleep(random.uniform(0.2, 0.6))

monitor = BufferMonitor(BUFFER_SIZE)

producers = [threading.Thread(target=producer, args=(monitor, i+1)) for i in range(3)]
consumers = [threading.Thread(target=consumer, args=(monitor, i+1)) for i in range(2)]

for p in producers:
    p.daemon = True
    p.start()

for c in consumers:
    c.daemon = True
    c.start()

time.sleep(SIMULATION_TIME)
print("\nSimulacao concluida.\n")