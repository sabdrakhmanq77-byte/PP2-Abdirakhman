from unittest import result


s=input()
if '+' in s:
    s.split('+')
if '-' in s:
    s.split('-')
if '*' in s:
    s.split('*')
def num(s):
    for i in range( 0, len(s), 3):
        x=s[i:i+3]
        result=[]
        mapping = {
        'ZER': 0, 'ONE': 1, 'TWO': 2, 'THR': 3, 'FOU': 4,
        'FIV': 5, 'SIX': 6, 'SEV': 7, 'EIG': 8, 'NIN': 9
        }
        if x in mapping:
            result.append(mapping[x])
    return result
num1=int(num(s[0]))
num2=int(num(s[1]))
if '+' in s:
        res=num1+num2
if '-' in s:
        res=num1-num2
if '*' in s:
        res=num1*num2
def res_to_str(res):
    mapping = {
        0: 'ZER', 1: 'ONE', 2: 'TWO', 3: 'THR', 4: 'FOU',
        5: 'FIV', 6: 'SIX', 7: 'SEV', 8: 'EIG', 9: 'NIN'
    }
    res_str = ''
    for digit in str(res):
        res_str += mapping[int(digit)]
    return res_str
print(res_to_str(res))
