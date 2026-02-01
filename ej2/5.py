num=int(input(''))
x=0
while 2**x<num:
    x+=1
if 2**x==num:
    print('YES')
else:
    print('NO')