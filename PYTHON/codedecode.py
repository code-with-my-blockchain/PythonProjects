import string
import random

st = input("Enter message: ")
words = st.split(" ")
coding = input("1 for Coding or 0 for Decoding: ")
coding = True if (coding=="1") else False
nwords = []
for word in words:
  if(len(word)>=3):
    if(coding):
      # Encoding Logic:
      # 1. Take the first letter and put it at the end
      # 2. Add 3 random characters at the start and end
      r1 = "dsf"
      r2 = "jkl"
      stnew = r1 + word[1:] + word[0] + r2
      nwords.append(stnew)
    
    else:
      # Decoding Logic
      stnew = word[3:-3]
      # Only rearrange if the word actually has letters left
      if len(stnew) > 0:
        stnew = stnew[-1] + stnew[:-1]
      nwords.append(stnew)
  else:
    # If word length is less than 3, just reverse it
    nwords.append(word[::-1])

print(" ".join(nwords))