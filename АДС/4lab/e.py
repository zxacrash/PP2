import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    for _ in range(n - 1):
        x = int(data[idx]); idx += 1
        y = int(data[idx]); idx += 1
        z = int(data[idx]); idx += 1
        if z == 0:
            left[x] = y
        else:
            right[x] = y

    best = 0
    queue = deque([1])
    while queue:
        sz = len(queue)
        best = max(best, sz)
        for _ in range(sz):
            node = queue.popleft()
            if left[node]:
                queue.append(left[node])
            if right[node]:
                queue.append(right[node])

    print(best)

main()