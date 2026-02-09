# *args and **kwargs allow functions to accept a unknown number of arguments.

def yc(*kids):
  print("The youngest child is " + kids[2])

yc("Emil", "Tobias", "Linus")

def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")

def maxn(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num

print(maxn(3, 7, 2, 9, 1))

def kwvar(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

kwvar(name = "Tobias", age = 30, city = "Bergen")
