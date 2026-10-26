a = int(input())

if a < 2:
    print("NO")
else:
    i = 2
    while i * i <= a:
        if a % i == 0:
            print("NO")
            break
        i += 1
    else:
        print("YES")