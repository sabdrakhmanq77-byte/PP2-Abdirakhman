def greet(name):  
    print(f"Hello, {name}!")

greet("Alice") #Hello, Alice!
greet("Bob") #Hello, Bob!

def add(a, b): #parameters
    print(a + b) #arguments

def my_function(person):
    print("Name:", person["name"])
    print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)
