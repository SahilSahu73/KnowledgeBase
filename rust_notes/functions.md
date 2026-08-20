# Functions
The `main` function is the entry point of the program.
Keyword `fn` allows you to declare new functions.

```rust
fn main() {
    print_labeled_measurement(5, 'h');
}

fn print_labeled_measurement(value: i32, unit_label: char) {
    println!("The measurement is: {value}{unit_label}");
}
```

- In functions signature, you must declare the type of each parameter.
- deliberate decision in rust design: Requiring type annotations in function definitions means the compiler almost never needs you to
use them elsewhere in the code to figure out what type you mean.

- Rust is an expression-based language
  - *Statements* are instructions that perform some action and do not return a value.
  - *Expressions* evaluate to a resultant value.

`let y = 6;` here the 6 is an expression that evaluates to a value of 6. Calling a function is an expression. Calling a macro is an
expression. A new scope block created with curly brackets is an expression as shown in the example below.
```rust
fn main() {
    let y = {
        let x = 3;
        x + 1
    };

    println!("The value of y is: {y}");
}
```
The expression in the above code example is a block that, in this case, evaluates to 4.
That value gets bound to `y` as part of the `let` statement.

> [!NOTE]
> The x+1 line is written without a semicolon at the end.
> Expressions do not include ending semicolons.
> If you add a semicolon to the end of an expression then you turn it into a statement, and it will then not return a value.

- Functions can return values to the code that calls them.
- We must declare their type after an arrow (`->`)
- In rust, the return value of the function is synonymous with the value of the final expression in the block of the body of the function.
- can return early from a function by using the `return` keyword and specifying a value, but most functions return the last expression
implicitly.

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();

    println!("The value of x is: {x}");
}
```
- in this example, there are no function calls, macros, or even let statements in the `five` function - just the number 5 by itself.
- it is still a valid function - there is a return type also specified in the function.
