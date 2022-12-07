import threading,time

start_time = time.perf_counter()

def math():
    a=1

def moreMath():
    a=1

th = []

for i in range(0,1000):
    th.append(threading.Thread(target= math))


for t in th:
    t.start()

for t in th:
    t.join()


finish_time = time.perf_counter()

print(f"it took {finish_time - start_time}s")
