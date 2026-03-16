N=int(input(''))
n=list(map(int,input('').split()))
sum=0
for i in n:
    sum=sum+(i**2)
print(sum)