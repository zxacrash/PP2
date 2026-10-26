import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    src = list(map(int, data[1:1 + n]))
    dst = [0] * n

    inv = 0
    width = 1
    while width < n:
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if src[i] <= src[j]:
                    dst[k] = src[i]
                    i += 1
                else:
                    dst[k] = src[j]
                    j += 1
                    inv += mid - i
                k += 1
            if i < mid:
                dst[k:k + mid - i] = src[i:mid]
                k += mid - i
            if j < hi:
                dst[k:k + hi - j] = src[j:hi]
        src, dst = dst, src
        width *= 2

    print(inv)

main()