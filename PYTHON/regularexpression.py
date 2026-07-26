# https://regex101.com/

import re

pattern = r"[A-Z]yclone"
text = '''Cyclone dumma damma Cyclone 
Dyclone lamma lamma Cyclone 
eyclone Cyclone 
Byclone Cyclone 
xyclone Cyclone 
Zyclone Cyclone 
'''

# match = re.search(pattern, text)
# print(match)

matches = re.finditer(pattern, text)
for match in matches:
  print(match.span())
  print(text[match.span()[0]:match.span()[1]])