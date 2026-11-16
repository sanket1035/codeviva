Program with 6 function(s) and 47 lines. (Offline mode: add GROQ_API_KEY for AI explanations.)

### `validate_amount()` (line 4)

`validate_amount` takes 1 input(s) (amount). Check that the amount is a positive number. It makes 1 decision(s) with if/else.

### `deposit()` (line 11)

`deposit` takes 2 input(s) (balance, amount). Add money to the balance. It makes 1 decision(s) with if/else. It calls `validate_amount`.

### `withdraw()` (line 18)

`withdraw` takes 2 input(s) (balance, amount). Remove money if the balance is enough. It makes 1 decision(s) with if/else. It calls `validate_amount`.

### `interest()` (line 25)

`interest` takes 3 input(s) (balance, rate, years). It uses 1 loop(s).

### `factorial()` (line 32)

`factorial` takes 1 input(s) (n). Recursive factorial. It makes 1 decision(s) with if/else. It calls `factorial`.

### `main()` (line 39)

`main` takes 0 input(s). It calls `deposit`, `withdraw`, `interest`, `factorial`.
