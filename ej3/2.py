def is_Usual(x):
    for factor in [2, 3, 5]:
        while x % factor == 0:
            x //= factor
        if x == 1:
            return True
    return False

N = int(input())
if is_Usual(N):
    print("Yes")
else:  
    print("No") 
 
