import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1

    values = []
    for _ in range(n):
        x1 = int(data[idx]); idx += 1
        y1 = int(data[idx]); idx += 1
        x2 = int(data[idx]); idx += 1
        y2 = int(data[idx]); idx += 1
        values.append(max(x2, y2))

    values.sort()
    print(values[k - 1])

main()