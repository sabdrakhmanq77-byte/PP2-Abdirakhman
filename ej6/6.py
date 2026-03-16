N=int(input(''))
num=list(map(int,input('').split()))
if all(n>=0 for n in num):
    print('Yes')
else:
    print('No')
