import sys
import bisect

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1

    a = list(map(int, data[idx:idx+n])); idx += n
    a.sort()

    def count(l, r):
        if l > r:
            return 0
        left = bisect.bisect_left(a, l)
        right = bisect.bisect_right(a, r)
        return right - left

    out = []
    for _ in range(q):
        l1 = int(data[idx]); idx += 1
        r1 = int(data[idx]); idx += 1
        l2 = int(data[idx]); idx += 1
        r2 = int(data[idx]); idx += 1

        c1 = count(l1, r1)
        c2 = count(l2, r2)
        inter = count(max(l1, l2), min(r1, r2))

        out.append(str(c1 + c2 - inter))

    print("\n".join(out))

main()