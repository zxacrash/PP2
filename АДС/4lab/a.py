import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    a = data[idx:idx+n]
    idx += n
    a = list(map(int, a))

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    root = 1
    for i in range(2, n + 1):
        val = a[i - 1]
        cur = root
        while True:
            if val <= a[cur - 1]:
                if left[cur] == 0:
                    left[cur] = i
                    break
                cur = left[cur]
            else:
                if right[cur] == 0:
                    right[cur] = i
                    break
                cur = right[cur]

    out = []
    for _ in range(m):
        path = data[idx].decode(); idx += 1
        cur = root
        ok = True
        for ch in path:
            if ch == 'L':
                cur = left[cur]
            else:
                cur = right[cur]
            if cur == 0:
                ok = False
                break
        out.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(out) + "\n")

main()
