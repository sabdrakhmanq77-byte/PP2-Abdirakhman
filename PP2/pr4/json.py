import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)   

# the result is a Python dictionary:
print(y["age"])
a= {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
b = json.dumps(x)

# the result is a JSON string:
print(b)

print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))


data = {
    "name": "John Doe",
    "age": 30,
    "is_student": False,
    "skills": ["Python", "Data Analysis", "Machine Learning"]
}
 
with open("output.json", "w") as file: #w means write mode, creates file if it doesnt exist or rewrites if it does
    json.dump(data, file, indent=4)

print("JSON file created successfully.")

with open("output.json", "r") as file: # Open the JSON file for reading
    data = json.load(file)

print(data)
print("Name:", data["name"])