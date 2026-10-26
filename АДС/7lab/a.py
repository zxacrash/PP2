import sys

def main():
    lines = sys.stdin.read().split('\n')
    t = int(lines[0])
    out = []
    for i in range(1, t + 1):
        words = lines[i].split()
        words.sort(key=len)
        out.append(" ".join(words))
    print("\n".join(out))

main()