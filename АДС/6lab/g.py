import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])

    cur_to_orig = {}
    idx = 1
    for _ in range(n):
        old = data[idx]
        new = data[idx + 1]
        idx += 2
        orig = cur_to_orig.pop(old, old)
        cur_to_orig[new] = orig

    res = sorted((orig, cur) for cur, orig in cur_to_orig.items())

    out = [str(len(res))]
    for orig, cur in res:
        out.append(f"{orig} {cur}")
    print("\n".join(out))

main()