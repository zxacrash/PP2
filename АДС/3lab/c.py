import sys
import bisect

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    a = data[idx:idx+n]
    idx += n
    a = list(map(int, a))

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    out = []
    for _ in range(m):
        b = int(data[idx]); idx += 1
        block = bisect.bisect_left(prefix, b)
        out.append(str(block))

    print("\n".join(out))

main()