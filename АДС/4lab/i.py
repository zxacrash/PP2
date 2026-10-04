import sys

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

    count = 0
    for i in range(n):
        if left[i] == -1 and right[i] == -1:
            count += 1

    print(count)

main()