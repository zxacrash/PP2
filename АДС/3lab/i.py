import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = list(map(int, data[idx:idx+n]))

    def blocks_needed(limit):
        blocks = 1
        cur = 0
        for x in a:
            if cur + x > limit:
                blocks += 1
                cur = x
            else:
                cur += x
        return blocks

    lo, hi = max(a), sum(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if blocks_needed(mid) <= k:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

main()