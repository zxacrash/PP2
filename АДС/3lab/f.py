import sys
import math

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    h = int(data[idx]); idx += 1
    bags = list(map(int, data[idx:idx+n]))

    def hours_needed(k):
        return sum((b + k - 1) // k for b in bags)

    lo, hi = 1, max(bags)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

main()