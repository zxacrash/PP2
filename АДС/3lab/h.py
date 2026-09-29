import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = list(map(int, data[idx:idx+n]))

    best = float('inf')
    left = 0
    cur_sum = 0

    for right in range(n):
        cur_sum += a[right]
        while cur_sum >= k:
            best = min(best, right - left + 1)
            cur_sum -= a[left]
            left += 1

    print(best)

main()