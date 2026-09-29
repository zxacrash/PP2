import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = list(map(int, data[idx:idx+n]))

    def pieces(length):
        return sum(int(x / length) for x in a)

    lo, hi = 0.0, max(a)
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid > 0 and pieces(mid) >= k:
            lo = mid
        else:
            hi = mid

    print(f"{lo:.9f}")

main()