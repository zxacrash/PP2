import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    idx = 1

    scale = {
        b"A+": 16, b"A": 15, b"B+": 14, b"B": 12,
        b"C+": 10, b"C": 8, b"D+": 6, b"D": 4, b"F": 0,
    }

    students = []
    for _ in range(n):
        last = data[idx]
        first = data[idx + 1]
        m = int(data[idx + 2])
        idx += 3
        q = 0
        den = 0
        for _ in range(m):
            c = int(data[idx + 1])
            q += scale[data[idx]] * c
            den += c
            idx += 2
        students.append((q / den, last, first))

    students.sort()

    out = [f"{l.decode()} {f.decode()} {g / 4:.3f}" for g, l, f in students]
    sys.stdout.write("\n".join(out) + "\n")

main()