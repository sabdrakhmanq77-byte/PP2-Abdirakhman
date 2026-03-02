# Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
import re
string='abbb'
x=re.search('ab{2,3}',string)

if x:
    print('Found in string')
else:
    print('Not found')