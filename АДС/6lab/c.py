import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = sorted(map(int, data[1:1 + n]))

    best = min(a[i + 1] - a[i] for i in range(n - 1))

    out = []
    for i in range(n - 1):
        if a[i + 1] - a[i] == best:
            out.append(a[i])
            out.append(a[i + 1])

    print(" ".join(map(str, out)))

main()