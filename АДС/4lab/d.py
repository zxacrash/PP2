import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    p = list(map(int, data[idx:idx+n])); idx += n

    t = [0] * (n + 1)
    for i, v in enumerate(p):
        t[v] = i + 1

    A = [t[v] for v in range(1, n + 1)]

    left = [-1] * n
    right = [-1] * n
    stack = []

    for i in range(n):
        last = -1
        while stack and A[stack[-1]] > A[i]:
            last = stack.pop()
        if stack:
            right[stack[-1]] = i
        if last != -1:
            left[i] = last
        stack.append(i)

    root = stack[0]

    level_sum = []
    q = deque([root])
    while q:
        s = 0
        nxt = deque()
        for _ in range(len(q)):
            node = q.popleft()
            s += node + 1
            if left[node] != -1:
                nxt.append(left[node])
            if right[node] != -1:
                nxt.append(right[node])
        level_sum.append(s)
        q = nxt

    print(len(level_sum))
    print(" ".join(map(str, level_sum)))

main()