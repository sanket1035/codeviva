"""Fibonacci (recursive and iterative) and prime numbers."""
import math


def fib_recursive(n):
    """n-th Fibonacci number using recursion."""
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    """n-th Fibonacci number using a loop."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def is_prime(n):
    """Trial division up to the square root."""
    if n < 2:
        return False
    for d in range(2, int(math.sqrt(n)) + 1):
        if n % d == 0:
            return False
    return True


def primes_upto(limit):
    return [n for n in range(2, limit + 1) if is_prime(n)]


def main():
    print([fib_recursive(i) for i in range(10)])
    print(fib_iterative(10))
    print(primes_upto(30))


if __name__ == "__main__":
    main()
