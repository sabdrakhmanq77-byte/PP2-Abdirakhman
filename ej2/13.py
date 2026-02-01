
import math


n=int(input(''))

if n <= 1:
    print('No')

if n == 2:
    print('Yes')
if n % 2 == 0:
    print('No')

for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            print('No')
            break
else:
    print('Yes')