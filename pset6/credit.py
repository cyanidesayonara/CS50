#import cs50
#
#while True:
#    print("Number: ", end="")
#    number = cs50.get_float()
#    if number >= 0:
#        break

# validate input
while True:
    cc = input("Number: ")
    if cc.isdecimal() and int(cc) > 0:
        break

# copy input into variables; lose last digit for int j
i, j = int(cc), int(cc) // 10
x1, x2 = 0, 0
    
# starting from last digit, add every other digit together
# % 10 yields last digit, // 100 "cuts off" last two
while i > 0:
    x1 += i % 10
    i //= 100
    
# starting from penultimate digit (already there), double every other digit, then add those digits together
while j > 0:
    # if result is not a single digit, % 10 yields last digit and // 10 yields the next one
    if (j % 10) * 2 > 8:
        x2 += ((j % 10) * 2) % 10
        x2 += ((j % 10) * 2) // 10
        j //= 100
    else:
        x2 += (j % 10) * 2
        j //= 100
        
checksum = x1 + x2

# if last digit of checksum = 0, and length and first digits are a match, print name
if checksum % 10 == 0:
    if len(cc) == 15 and cc[:2] == "34" or cc[:2] == "37":
        print("AMEX")
    elif len(cc) == 16 and cc[:2] == "51" or cc[:2] == "52" or cc[:2] == "53" or cc[:2] == "54" or cc[:2] == "55":
        print("MASTERCARD")
    elif len(cc) == 13 or len(cc) == 16 and cc[:1] == "4":
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")