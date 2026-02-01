par=list(map(int, input('').split( )))
s=list(map(int, input('').split( )))
s.reverse(par[1]-1, par[2]+1)
print(*s)