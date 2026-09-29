import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    queries = data[idx:idx+t]; idx += t
    queries = list(map(int, queries))

    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    a = []
    for i in range(n):
        row = list(map(int, data[idx:idx+m]))
        idx += m
        a.append(row)

    row_low = [0] * n
    row_high = [0] * n
    for i in range(n):
        first, last = a[i][0], a[i][-1]
        if first < last:
            row_low[i], row_high[i] = first, last
        else:
            row_low[i], row_high[i] = last, first

    def find_row(v):
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if row_low[mid] <= v <= row_high[mid]:
                return mid
            elif v > row_high[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        return -1

    def find_col(r, v):
        lo, hi = 0, m - 1
        row = a[r]
        if r % 2 == 0:
            while lo <= hi:
                mid = (lo + hi) // 2
                if row[mid] == v:
                    return mid
                elif row[mid] > v:
                    lo = mid + 1
                else:
                    hi = mid - 1
        else:
            while lo <= hi:
                mid = (lo + hi) // 2
                if row[mid] == v:
                    return mid
                elif row[mid] < v:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1

    out = []
    for v in queries:
        r = find_row(v)
        if r == -1:
            out.append("-1")
            continue
        c = find_col(r, v)
        if c == -1:
            out.append("-1")
        else:
            out.append(f"{r} {c}")

    print("\n".join(out))

main()