# Write a Python program to split a string at uppercase letters.
import re
string='ThisIsAStringWithUpperCaseLetters'
x=re.split('[A-Z]',string)
print(x)
