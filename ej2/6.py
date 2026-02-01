n=int(input(''))
numbers=list(map(int, input('').split()))
max_num=numbers[0]
pos=0
max_pos=1
for i in numbers:
    pos+=1
    if i>max_num:
        max_num=i
        max_pos=pos
print(max_pos)
        
