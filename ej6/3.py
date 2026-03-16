N=int(input(''))
words=list(input('').split())
s=[]
for i,word in enumerate(words):
    s.append(f'{i}:{word}')
print(*s)