import sys
import bisect

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    k = data[1 + n]

    i = bisect.bisect_right(a, k)
    print(a[i] if i < n else a[0])

main()