import os
import shutil

os.makedirs("myFolder", exist_ok=True)
shutil.move("a.txt","myFolder/a.txt")
