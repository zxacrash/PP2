import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    dates = data[1:1 + n]

    dates.sort(key=lambda s: (s[6:10], s[3:5], s[0:2]))

    print("\n".join(dates))

main()