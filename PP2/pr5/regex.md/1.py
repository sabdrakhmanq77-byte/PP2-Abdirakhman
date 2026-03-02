# Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re

string='abbbb'
strings='a'
srtingt='dsss'

x=re.search('ab*',string)
y=re.search('ab*',strings)
z=re.search('ab*',srtingt)
if x:
    print('Found in string')
if y:
    print('Found in strings')
if z:
    print('Found in srtingt')
else:
    print('Not found')