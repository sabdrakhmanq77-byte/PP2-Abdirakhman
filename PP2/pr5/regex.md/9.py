# Write a Python program to insert spaces between words starting with capital letters.
import re
string='ThisIsAStringWithCapitalLetters'
x=re.sub('([A-Z])', r' \1', string)
print(x)