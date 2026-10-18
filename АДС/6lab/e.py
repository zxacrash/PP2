import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    vals = list(map(int, data[2:2 + n * m]))

    cols = []
    for j in range(m):
        col = vals[j::m]
        col.sort(reverse=True)
        cols.append(col)

    out = []
    for i in range(n):
        out.append(" ".join(str(cols[j][i]) for j in range(m)))

    print("\n".join(out))

main()