import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    a = list(map(int, data[idx:idx+n])); idx += n
    k = int(data[idx]); idx += 1

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    root = 1
    for i in range(2, n + 1):
        val = a[i - 1]
        cur = root
        while True:
            if val < a[cur - 1]:
                if left[cur] == 0:
                    left[cur] = i
                    break
                cur = left[cur]
            else:
                if right[cur] == 0:
                    right[cur] = i
                    break
                cur = right[cur]

    start = root
    while a[start - 1] != k:
        if k < a[start - 1]:
            start = left[start]
        else:
            start = right[start]

    out = []
    stack = [start]
    while stack:
        node = stack.pop()
        out.append(str(a[node - 1]))
        if right[node]:
            stack.append(right[node])
        if left[node]:
            stack.append(left[node])

    print(" ".join(out))

main()