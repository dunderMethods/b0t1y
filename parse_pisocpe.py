import matplotlib.pyplot as plt
import numpy as np
data = []
with open(r'Dumps\botley_logs\send_empty_queue.txt', 'r') as f:
    data = f.readlines()


end_length = 32
#
# hex_as_int = int(hexadecimal, 16)
#
# hex_as_binary = bin(hex_as_int)
#
# padded_binary = hex_as_binary[2:].zfill(end_length)

pdata = [line.strip('\n').split(' ') for line in data[3:]]

pdata = [[int(line[0]), int(line[1], 16)] for line in pdata]
print(pdata[:5])
pdata = np.array(pdata)
x,y = pdata[:, 0], pdata[:, 1]

thresh = int(np.mean(x))

y_mod = [0 if val < thresh else 1 for val in y]

plt.plot(x,y)
plt.show()