import sys

def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    a = list(map(int, data[idx:idx+n])); idx += n
    p_count = int(data[idx]); idx += 1
    p = list(map(int, data[idx:idx+p_count])); idx += p_count

    MAX_VAL = 1000
    cnt = [0] * (MAX_VAL + 1)
    total = [0] * (MAX_VAL + 1)

    for x in a:
        cnt[x] += 1
        total[x] += x

    for v in range(1, MAX_VAL + 1):
        cnt[v] += cnt[v - 1]
        total[v] += total[v - 1]

    out = []
    for power in p:
        out.append(f"{cnt[power]} {total[power]}")

    print("\n".join(out))

main()