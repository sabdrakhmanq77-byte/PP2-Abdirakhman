def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

# OR

def get_greeting():
  return "Hello from a function"

print(get_greeting())

# Function definitions cannot be empty. If you need to create a function placeholder without any code, use the pass statement:

def my_function():
  pass