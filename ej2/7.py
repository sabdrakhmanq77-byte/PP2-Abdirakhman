N=int(input(''))
s=[]
i=0
while 2**i<=N:
    s.append(2**i)
    i+=1
print(*s)