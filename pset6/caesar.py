import sys

# make sure argument count is 2 and second argument (key) is int
if len(sys.argv) == 2 and sys.argv[1].isdecimal():
    key = int(sys.argv[1]) % 26
else:
    print ("Usage: python caesar.py [int]")
    sys.exit(1)

# input must not be empty
while True:
    plain = input("plaintext: ")
    if plain != "":
        break

print ("ciphertext: ", end="")    
    
# list letters in order
uppers = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
lowers = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
# iterate over characters;
for c in plain:
    if c.isalpha():
        if c.isupper():
            # lower case character - 65 is index on list; add key; mod 26 to wrap around
            letter = (uppers[(ord(c) - 65 + key) % 26])
            print (letter, end="")
        elif c.islower():
            # upper case character - 97 is index on list; add key; mod 26 to wrap around
            letter = (lowers[(ord(c) - 97 + key) % 26])
            print (letter, end="")
    else:
        print (c, end="")
        
print("")