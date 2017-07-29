x = 1
x = str(5 + 1) + ",7"
fPart = " "
for i in range (len(x)):
	if x[i] == ",":
		index = i 
		#print index
fPart = x[:index]
lPart = x[index+1:]

print int(fPart)
print int(lPart)

#y = x[]
