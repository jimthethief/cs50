import cs50

# Check input is valid
while True:
    # Get input
    height = cs50.get_int("Height: ")
    if height < 9 and height > 0:
        break

# Starting values
space = height - 1
block = 1
counter = 0

# Make pyramid
for i in range(height):
    print(" " * space, end="")
    print("#" * block, end="")
    print("  ", end="")
    print("#" * block, end="")
    print()
    space -= 1
    block += 1