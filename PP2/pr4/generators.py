# #Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers which you can get an iterator from.

# mytuple = ("apple", "banana", "cherry")
# myit = iter(mytuple)

# print(next(myit))
# print(next(myit))
# print(next(myit))

# for x in mytuple:
#   print(x)

# class MyNumbers:     #make iterator
#   def __iter__(self):
#     self.a = 1
#     return self

#   def __next__(self): #made next method
#     if self.a <= 20:
#       x = self.a
#       self.a += 1
#       return x
#     else:
#       raise StopIteration # by setting a condition we can make the stopiterator

# myclass = MyNumbers()
# myiter = iter(myclass)

# for x in myiter:
#   print(x)

# #creating generator object
# squarenum=(x*x for x in range(10))
# for i in squarenum:
#     print(i)
# #generators as functions
# def my_gen():
#     n=0
#     while n<10:
#         yield n
#         n+=1
# for i in my_gen():
#     print(i)

N=int(input(''))
square=(x**2 for x in range(N))
for i in square:
    print(i)

n=int(input(''))
def my_gen(n):
    for i in range(n):
        if i%2==0:
            yield i
print(",".join(str(i) for i in my_gen(n)))

def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for number in divisible_by_3_and_4(n):
    print(number)

a=int(input(''))
b=int(input(''))
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

for value in squares(1, 5):
    print(value)

def countdown(n):
    while n >= 0:
        yield n
        n -= 1

for number in countdown(5):
    print(number)