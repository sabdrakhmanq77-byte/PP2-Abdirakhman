N=int(input(''))
words=list(input('').split())
s=[]
for i,word in enumerate(words):
    s.append(f'{i}:{word}')
print(*s)
A=list(map(int,input('').split()))
B=list(map(int,input('').split()))
result=sum(a*b for a,b in zip(A,B))
print(result)
