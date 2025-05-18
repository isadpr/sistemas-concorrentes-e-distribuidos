import threading
import time
import random
from queue import Queue

BUFFER_SIZE = 5
NUM_PRODUCERS = 3
NUM_CONSUMERS = 2
SIMULATION_TIME = 10

buffer = Queue(BUFFER_SIZE)
mutex = threading.Semaphore(1)
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

class Producer(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        
    def run(self): 
        while True:
            item = random.randint(1, 100)
            time.sleep(random.uniform(0.1, 0.5))
            
            empty.acquire()
            mutex.acquire()
            
            buffer.put(item)
            print(f"Produtor {self.id} produziu: {item} | Buffer: {list(buffer.queue)}")
            
            mutex.release()
            full.release()

class Consumer(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        
    def run(self):
        while True:
            time.sleep(random.uniform(0.1, 0.8))
            
            full.acquire()
            mutex.acquire() 
            
            item = buffer.get()
            print(f"Consumidor {self.id} consumiu: {item} | Buffer: {list(buffer.queue)}")
            
            mutex.release()  
            empty.release()
            
            
            time.sleep(random.uniform(0.2, 0.6))

producers = [Producer(i+1) for i in range(NUM_PRODUCERS)]
consumers = [Consumer(i+1) for i in range(NUM_CONSUMERS)]

for p in producers:
    p.daemon = True
    p.start()

for c in consumers:
    c.daemon = True
    c.start()

time.sleep(SIMULATION_TIME)
print("\nSimulacao concluida.\n")