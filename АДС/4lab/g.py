import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    vals = list(map(int, data[idx:idx+n])); idx += n

    MAXN = n + 1
    node_val = [0] * MAXN
    left = [0] * MAXN
    right = [0] * MAXN
    parent = [0] * MAXN
    seen = {}

    cnt = 0
    root = 0
    for v in vals:
        if v in seen:
            continue
        cnt += 1
        node_val[cnt] = v
        seen[v] = cnt
        if root == 0:
            root = cnt
            continue
        cur = root
        while True:
            if v < node_val[cur]:
                if left[cur] == 0:
                    left[cur] = cnt
                    parent[cnt] = cur
                    break
                cur = left[cur]
            else:
                if right[cur] == 0:
                    right[cur] = cnt
                    parent[cnt] = cur
                    break
                cur = right[cur]

    def bfs(start):
        dist = [-1] * (cnt + 1)
        dist[start] = 0
        q = deque([start])
        farthest = start
        while q:
            u = q.popleft()
            for w in (left[u], right[u], parent[u]):
                if w != 0 and dist[w] == -1:
                    dist[w] = dist[u] + 1
                    if dist[w] > dist[farthest]:
                        farthest = w
                    q.append(w)
        return farthest, dist

    u, _ = bfs(root)
    v, dist = bfs(u)
    print(dist[v] + 1)

main()