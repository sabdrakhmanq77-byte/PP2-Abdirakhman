class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)

class person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = person("Emil")
p2 = Person("Tobias", 25)
    
print(p1.name, p1.age)
print(p2.name, p2.age)