f = open('myfile.txt', 'r')
i = 0
while True:
  i = i + 1
  line = f.readline()
  if not line:
    break
  try:
    parts = line.split(",")
    m1 = int(parts[0])
    m2 = int(parts[1])
    m3 = int(parts[2])
    print(f"Marks of student {i}: {m1}, {m2}, {m3}")
  except (ValueError, IndexError):
    print(f"Line {i} skip kar di gayi kyunki format sahi nahi tha: {line.strip()}")

f.close()