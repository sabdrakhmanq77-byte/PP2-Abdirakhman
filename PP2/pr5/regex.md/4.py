# Write a Python program to find the sequences of one upper case letter followed by lower case letters.

import re
string='AAAAAAAAaaaaaaa'
x=re.findall('[A-Z][a-z]+',string)
print(x)