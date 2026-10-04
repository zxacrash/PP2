import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    a = list(map(int, data[idx:idx+n])); idx += n

    if k > n:
        print(-1)
        return

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    root = 1
    for i in range(2, n + 1):
        val = a[i - 1]
        cur = root
        while True:
            if val < a[cur - 1]:
                if left[cur] == 0:
                    left[cur] = i
                    break
                cur = left[cur]
            else:
                if right[cur] == 0:
                    right[cur] = i
                    break
                cur = right[cur]

    stack = []
    node = root
    count = 0
    ans = -1
    while stack or node:
        while node:
            stack.append(node)
            node = left[node]
        node = stack.pop()
        count += 1
        if count == k:
            ans = a[node - 1]
            break
        node = right[node]

    print(ans)

main()