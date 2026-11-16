**Q1. What does the function `fib_recursive` do?**

`fib_recursive` takes 1 input(s) (n). n-th Fibonacci number using recursion. It makes 1 decision(s) with if/else. It calls `fib_recursive`.

**Q2. Which functions does `fib_recursive` call and why?**

It calls fib_recursive.

**Q3. What does the function `fib_iterative` do?**

`fib_iterative` takes 1 input(s) (n). n-th Fibonacci number using a loop. It uses 1 loop(s).

**Q4. What does the function `is_prime` do?**

`is_prime` takes 1 input(s) (n). Trial division up to the square root. It uses 1 loop(s). It makes 2 decision(s) with if/else.

**Q5. What does the function `primes_upto` do?**

`primes_upto` takes 1 input(s) (limit). It calls `is_prime`.

**Q6. Which functions does `primes_upto` call and why?**

It calls is_prime.

**Q7. What does the function `main` do?**

`main` takes 0 input(s). It calls `fib_iterative`, `primes_upto`, `fib_recursive`.

**Q8. Which functions does `main` call and why?**

It calls fib_iterative, primes_upto, fib_recursive.
