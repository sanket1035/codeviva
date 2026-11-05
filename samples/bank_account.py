"""Simple bank account lab program."""


def validate_amount(amount):
    """Check that the amount is a positive number."""
    if amount <= 0:
        return False
    return True


def deposit(balance, amount):
    """Add money to the balance."""
    if validate_amount(amount):
        return balance + amount
    return balance


def withdraw(balance, amount):
    """Remove money if the balance is enough."""
    if validate_amount(amount) and amount <= balance:
        return balance - amount
    return balance


def interest(balance, rate, years):
    total = balance
    for _ in range(years):
        total = total + total * rate / 100
    return total


def factorial(n):
    """Recursive factorial."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def main():
    bal = 1000
    bal = deposit(bal, 500)
    bal = withdraw(bal, 200)
    print(interest(bal, 5, 3))
    print(factorial(5))


main()
