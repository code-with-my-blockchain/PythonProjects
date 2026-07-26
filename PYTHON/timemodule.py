import time 

# time.time()
def init():
  for i in range(5000):
    print(i)

init()
t1 = time.time()
init()
print(time.time() - t1)

t = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

print(formatted_time)