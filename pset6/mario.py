while True:
    height = int(input("Height: "))
    if height > 0 or height < 24:
        break

# iterate from i = 1 to i = height + 1
for i in range (1, height + 1):
    print(" " * (height - i), end="")
    print("#" * (i), end="")
    print(" " * 2, end="")
    print("#" * (i))