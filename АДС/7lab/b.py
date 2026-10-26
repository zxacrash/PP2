import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    m = int(data[1 + n])
    b = list(map(int, data[2 + n:2 + n + m]))

    res = []
    i = j = 0
    while i < n and j < m:
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res.extend(a[i:])
    res.extend(b[j:])

    print(" ".join(map(str, res)))

main()