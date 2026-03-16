numbers=[1,2,3,4,5]
def odd(x):
    if x%2!=0:
        return False
    else:        return True
odd=filter(odd,numbers)
print(map(lambda x:x,odd))