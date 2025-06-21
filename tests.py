import numpy as np



z = np.random.randint(0, 256, size=(16,16,3), dtype=int)

i=0
for row in z:
  for column in row:
    if (column == 0).all():
      print(i)
      i+=1