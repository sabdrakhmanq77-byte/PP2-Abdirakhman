import os

if not os.path.exists("myFolder"):
  os.mkdir("myFolder")

print(os.listdir())
