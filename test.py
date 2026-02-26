import random

blocks = [[[0 # block number
    for z in range (16)]
    for y in range (16)]
    for x in range (16)]

blocks[0][0][0] = random.choices([0, 9, 10], [20, 2, 1])[0]

print(random.choices([0, 9, 10], [20, 2, 1])[0])