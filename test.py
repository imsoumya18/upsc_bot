x = '--send [123, 125, 127] hi how are you'
msg = x[x.find(']')+2:]
x = x[x.find('[')+1: x.find(']')].split(', ')
xint = []
for i in x:
    xint.append(int(i))
print(xint)
print(msg)
