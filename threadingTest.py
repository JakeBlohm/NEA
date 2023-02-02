def foo(bar, result, index):
    print (f"hello {bar}")
    result[index] = "foo"

from threading import Thread

results = [None] * 10

for i in range(len(threads)):
    threads[i] = Thread(target=foo, args=('world!', results, i))
    threads[i].start()

# do some other stuff

for i in range(len(threads)):
    threads[i].join()

print ((results))  # what sound does a metasyntactic locomotive make?