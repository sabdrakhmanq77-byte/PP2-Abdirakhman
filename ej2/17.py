N=int(input(''))
s=[]
for i in range(0, N):
    s.append(int(input('')))
dif_num=dict()
count=0
for i in s:
    dif_num[i]=dif_num.get(i,0)+1
for i in dif_num:
    if dif_num[i]==3:
        count+=1
print(count)
    


