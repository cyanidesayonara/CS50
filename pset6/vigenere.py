import sys

# make sure argument count is 2 and second argument (key) is a string of alphas
if len(sys.argv) == 2 and sys.argv[1].isalpha():
    key = str.lower(sys.argv[1])
else:
    print ("Usage: python viginere.py [string]")
    sys.exit(1)
    
# plaintext input mustn't be empty
while True:
    plain = input("plaintext: ")
    if plain != "":
        break

print ("ciphertext: ", end="")

# list letters in order
uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowers = "abcdefghijklmnopqrstuvwxyz"

# there must be a neater way to do this
i = 0

# iterate over characters;
for c in plain:
    if c.isalpha():
        if c.isupper():
            # the formula is: upper character - 65; add key[index % length of key] - 97 (always lower); mod 26
            print ((uppers[(ord(c) - 65 + ord(key[i % len(key)]) - 97) % 26]), end="")
        elif c.islower():
            # the formula is: lower character - 97; add key[index % length of key] - 97 (always lower); mod 26
            print ((lowers[(ord(c) - 97 + ord(key[i % len(key)]) - 97) % 26]), end="")
        i += 1
    else:
        print (c, end="")
        
print("")