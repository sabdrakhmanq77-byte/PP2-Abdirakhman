# Write a Python program to find sequences of lowercase letters joined with a underscore.
import re
string='aaa__bbb_cc' 
x=re.findall('[a-z]+[a-z]+',string)
print(x)
