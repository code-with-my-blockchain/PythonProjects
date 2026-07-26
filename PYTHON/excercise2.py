import random
import string

def generate_random_chars():
    return ''.join(random.choices(string.ascii_lowercase, k=3))

st = input("Enter message: ") # Yahan aap apna NAME ya koi bhi MESSAGE likhenge
words = st.split(" ")
command = input("Type '1' for Coding or '0' for Decoding: ")
coding = True if (command == "1") else False

if(coding):
    nwords = []
    for word in words:
        if(len(word) >= 3):
            r1 = generate_random_chars()
            r2 = generate_random_chars()
            stnew = r1 + word[1:] + word[0] + r2
            nwords.append(stnew)
        else:
            nwords.append(word[::-1])
    print("Encoded Message: ", " ".join(nwords))

else:
    nwords = []
    for word in words:
        if(len(word) >= 3):
            stnew = word[3:-3]
            stnew = stnew[-1] + stnew[:-1]
            nwords.append(stnew)
        else:
            nwords.append(word[::-1])
    print("Decoded Message: ", " ".join(nwords))
    