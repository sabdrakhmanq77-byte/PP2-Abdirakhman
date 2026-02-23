#Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers which you can get an iterator from.

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

for x in mytuple:
  print(x)

class MyNumbers:     #make iterator
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self): #male next method
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration # by setting a condition we can make the stopiterator

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)

#creating generator object
squarenum=(x*x for x in range(10))
for i in squarenum:
    print(i)
#generators as functions
def my_gen():
    n=0
    while n<10:
        yield n
        n+=1
for i in my_gen():
    print(i)