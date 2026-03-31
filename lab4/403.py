a = int (input ())
print(*(i for i in range(a+1) if i % 12 == 0))