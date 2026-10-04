import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    raw = list(map(int, data[idx:idx+n])); idx += n

    t = {}
    order = 0
    for v in raw:
        if v not in t:
            order += 1
            t[v] = order

    sorted_vals = sorted(t.keys())
    m = len(sorted_vals)
    A = [t[v] for v in sorted_vals]

    left = [-1] * m
    right = [-1] * m
    stack = []

    for i in range(m):
        last = -1
        while stack and A[stack[-1]] > A[i]:
            last = stack.pop()
        if stack:
            right[stack[-1]] = i
        if last != -1:
            left[i] = last
        stack.append(i)

    root = stack[0]

    adj = [[] for _ in range(m)]
    for i in range(m):
        if left[i] != -1:
            adj[i].append(left[i])
            adj[left[i]].append(i)
        if right[i] != -1:
            adj[i].append(right[i])
            adj[right[i]].append(i)

    def bfs(start):
        dist = [-1] * m
        dist[start] = 0
        q = deque([start])
        farthest = start
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] == -1:
                    dist[w] = dist[u] + 1
                    if dist[w] > dist[farthest]:
                        farthest = w
                    q.append(w)
        return farthest, dist

    u, _ = bfs(root)
    v, dist = bfs(u)
    print(dist[v] + 1)

main()