n = int(input())
a = list(map(int, input().split()))
x = int(input())

lo, hi = 0, n - 1
found = False
while lo <= hi:
    mid = (lo + hi) // 2
    if a[mid] == x:
        found = True
        break
    elif a[mid] < x:
        lo = mid + 1
    else:
        hi = mid - 1

print("Yes" if found else "No")