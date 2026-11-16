**Q1. What does the function `validate_amount` do?**

`validate_amount` takes 1 input(s) (amount). Check that the amount is a positive number. It makes 1 decision(s) with if/else.

**Q2. What does the function `deposit` do?**

`deposit` takes 2 input(s) (balance, amount). Add money to the balance. It makes 1 decision(s) with if/else. It calls `validate_amount`.

**Q3. Which functions does `deposit` call and why?**

It calls validate_amount.

**Q4. What does the function `withdraw` do?**

`withdraw` takes 2 input(s) (balance, amount). Remove money if the balance is enough. It makes 1 decision(s) with if/else. It calls `validate_amount`.

**Q5. Which functions does `withdraw` call and why?**

It calls validate_amount.

**Q6. What does the function `interest` do?**

`interest` takes 3 input(s) (balance, rate, years). It uses 1 loop(s).

**Q7. What does the function `factorial` do?**

`factorial` takes 1 input(s) (n). Recursive factorial. It makes 1 decision(s) with if/else. It calls `factorial`.

**Q8. Which functions does `factorial` call and why?**

It calls factorial.

**Q9. What does the function `main` do?**

`main` takes 0 input(s). It calls `deposit`, `withdraw`, `interest`, `factorial`.

**Q10. Which functions does `main` call and why?**

It calls deposit, withdraw, interest, factorial.
