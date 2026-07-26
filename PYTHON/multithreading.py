import threading
import time

# Indicates some task being done
def func(seconds):
  print(f"Sleeping for {seconds} seconds")
  time.sleep(seconds)
  return seconds

def main():
  time1 = time.perf_counter()
  # Normal Code
  # func(4) 
  # func(2)
  # func(1)
  
  
  # Same code using Threads
  t1 = threading.Thread(target=func, args=[4])
  t2 = threading.Thread(target=func, args=[2])
  t3 = threading.Thread(target=func, args=[1])
  
  t1.start()
  t2.start()
  t3.start()
  
  t1.join()
  t2.join()
  t3.join()
  # Calculating Time 
  time2 = time.perf_counter()
  print(time2 - time1)

main()

import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Indicates some task being done
def func(seconds):
  print(f"Sleeping for {seconds} seconds")
  time.sleep(seconds)
  return seconds

def poolingDemo():
  with ThreadPoolExecutor() as executor:
    # Method 1: Submitting tasks individually
    # f1 = executor.submit(func, 3)
    # f2 = executor.submit(func, 2)
    # f3 = executor.submit(func, 4)
    # print(f1.result())
    # print(f2.result())
    # print(f3.result())
    
    # Method 2: Using map to run multiple arguments
    l = [3, 5, 1, 2]
    results = executor.map(func, l)
    for result in results:
      print(result)

poolingDemo()