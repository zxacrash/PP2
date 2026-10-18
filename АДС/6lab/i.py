import sys

def main():
    s = sys.stdin.readline().strip()

    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    out = []
    for i in range(26):
        out.append(chr(ord('a') + i) * cnt[i])

    print("".join(out))

main()