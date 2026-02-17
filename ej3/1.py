def isVal(x):
    while x>0:
        digit = x % 10
        if digit%2!=0:
            return "Not valid"
        x = x // 10
    return "Valid"

N = int(input())
print(isVal(N))