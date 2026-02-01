N=int(input(''))
s=list(map(int, input().split()))
for i in range(0, len(s)):
    s[i]=s[i]**2
print(*s)