import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    res = [0] * n
    l, r = 0, n - 1
    for k in range(n - 1, -1, -1):
        if abs(a[l]) > abs(a[r]):
            res[k] = a[l] * a[l]
            l += 1
        else:
            res[k] = a[r] * a[r]
            r -= 1

    print(" ".join(map(str, res)))

main()