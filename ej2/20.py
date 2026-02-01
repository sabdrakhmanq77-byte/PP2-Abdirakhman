n=int(input(''))
doc=dict()
for i in range(n):
    command=input('').split()
    if command[0]=='set':
        doc[command[1]]=command[2]
    elif command[0]=='get':
        if command[1] in doc:
            print(doc[command[1]])
        else:
            print(f'KE: no key {command[1]} found in the document')