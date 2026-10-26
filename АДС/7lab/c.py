import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    vals = list(map(int, data[2:2 + n * m]))

    rows = [vals[i * m:(i + 1) * m] for i in range(n)]
    rows.sort(key=lambda r: (-sum(r), r))

    print("\n".join(" ".join(map(str, r)) for r in rows))

main()