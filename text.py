
abc = "12.34"
index = abc.rfind(".")
print(abc[index-1])
print(abc[index+1])
digit1 = abc[index - 1]
digit2 = abc[index + 1]

print(digit1.isdigit())
print(digit2.isdigit())
