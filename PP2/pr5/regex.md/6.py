# Write a Python program to replace all occurrences of space, comma, or dot with a colon.

import re
string='This is a string, with spaces, commas, and dots.'
x=re.sub('[ ,.]',':',string)
print(x)