from random import randint
from sys import exit

pin = randint(0000, 9999)

for num in range(0000, 10000):
    print(f"Checking {num:04}...")
    if num == pin:
        print(f"FOUND! Pin is {num:04}")
        exit(1)