import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    a = data[2:2 + n]
    b = data[2 + n:2 + n + m]

    common = Counter(map(int, a)) & Counter(map(int, b))
    res = sorted(common.elements())

    print(" ".join(map(str, res)))

main()