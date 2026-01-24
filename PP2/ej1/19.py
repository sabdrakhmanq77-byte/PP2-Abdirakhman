sen=input('')
tar=input('')
repl=input('')
if tar in sen:
    sen=sen.replace(tar, repl)
print(sen)