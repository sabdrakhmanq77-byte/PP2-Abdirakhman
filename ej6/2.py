N=int(input(''))
n=list(map(int,input().split()))
count=0
for i in n:
    if i%2==0:
        count+=1
print(count)