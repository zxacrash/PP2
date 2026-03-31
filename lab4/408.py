def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def prime_generator(n):
    for i in range(1, n + 1):
        if is_prime(i):
            yield i
try:
    n = int(input())
    print(*(prime_generator(n)))
except EOFError:
    pass