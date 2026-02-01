n=int(input(''))
count=0
numbers = list(map(int, input("").split()))
for i in numbers:
    if i>0:
        count+=1
print(count)