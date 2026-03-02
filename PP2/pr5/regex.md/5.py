# Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.

import re
string='aaaabrrrrrrrb'
x=re.findall('a.*b',string)
print(x)