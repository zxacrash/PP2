import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    a = list(map(int, data[idx:idx+n])); idx += n

    # Сортируем позиции: по значению, а при равенстве — по убыванию порядка вставки
    # (позже вставленный дубликат оказывается левее в BST)
    order = sorted(range(n), key=lambda i: (a[i], -(i + 1)))
    P = [order[j] + 1 for j in range(n)]  # порядок вставки (приоритет) в отсортированном порядке

    left_s = [-1] * n
    right_s = [-1] * n
    stack = []

    for i in range(n):
        last = -1
        while stack and P[stack[-1]] > P[i]:
            last = stack.pop()
        if stack:
            right_s[stack[-1]] = i
        if last != -1:
            left_s[i] = last
        stack.append(i)

    root_sorted = stack[0]

    left = [0] * (n + 1)
    right = [0] * (n + 1)
    for pos in range(n):
        orig = order[pos] + 1
        if left_s[pos] != -1:
            left[orig] = order[left_s[pos]] + 1
        if right_s[pos] != -1:
            right[orig] = order[right_s[pos]] + 1

    root = order[root_sorted] + 1

    out = []
    for _ in range(m):
        path = data[idx].decode(); idx += 1
        cur = root
        ok = True
        for ch in path:
            cur = left[cur] if ch == 'L' else right[cur]
            if cur == 0:
                ok = False
                break
        out.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(out) + "\n")

main()