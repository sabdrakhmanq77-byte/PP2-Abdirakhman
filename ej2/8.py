N=int(input(''))
s=[]
s = list(map(int, input().split()))
min_val=s[0]
max_val=s[0]
for i in s:
    if i<min_val:
        min_val=i
    if i>max_val:
        max_val=i
for i in range(0, len(s)):
    if s[i]==max_val:
        s[i]=min_val
print(*s)