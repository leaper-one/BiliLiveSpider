import queue

q = queue.Queue()

list = [['1234', 10], ['1234', 20], ['3456', 100]]

uid = ''
for i in list:
    if i[0] == uid:



print(q.empty())
print(q.qsize())

for i in range(q.qsize()):
    print(q.get())