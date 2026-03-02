# Write a Python program to convert a given camel case string to snake case.
import re
string='ThisIsACamelCaseString'
x=re.sub('([A-Z])', r'_\1', string).lower()
print(x)    
