n, q = map(int, input().split())
a = list(map(int, input().split()))

out = []
for _ in range(q):
    l1, r1, l2, r2 = map(int, input().split())
    count = 0
    for c in a:
        if (l1 <= c <= r1) or (l2 <= c <= r2):
            count += 1
    out.append(str(count))

print("\n".join(out))