# Write a python program to convert snake case string to camel case string.
import re
string='this_is_a_snake_case_string'
x=re.sub('(_.)',lambda x:x.group(1)[1].upper(),string)
print(x)