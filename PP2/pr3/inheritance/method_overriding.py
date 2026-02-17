class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)
class Student(Person):
  def __init__(self, fname, lname):
      Person.__init__(self, fname, lname)
# By calling the __init__() function of the parent class, we can access the properties of the parent class in the child class.