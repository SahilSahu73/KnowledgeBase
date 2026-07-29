# Variables and Mutability
Variables are immutable by default.
When a var is immutable, once a value is bound to a name, you can't change that value.

```rust
fn main(){
  let x = 5;
  println!("The value of x is: {x}");
  x = 6;
  println!("The value of x is: {x}");
}
```
> cargo run

This will return an error:
error[E0384]: cannot assign twice to immutable variable 'x'
because we tried to assign a second value to the immutable variable 'x'.

Can make the variables mutable by adding the keyword `mut` in front of the variable name.
Adding `mut` also conveys intent to future readers of the code by indicating that other parts of the code
will be changing this variable's value.

```rust
fn main(){
  let mut x = 5;
  println!("The value of x is: {x}");
  x = 6;
  println!("The value of x is: {x}");
}
```
> cargo run

Now this code will compile and print the answers, i.e. initially x is 5 and then x is 6.

## Declaring Constants
Like immutable variables, *constants* are values that are bound to and are not allowed to change, but there are a few differences.
1. Not allowed to use `mut` with constants.
They are always immutable.
Declared using the keyword `const` instead of the `let` keyword, and the type of the value must always be annotated.
2. Constants can be declared in any scope, including the global scope, which makes it useful for other parts of the code to know.
3. Constants may be set only to a constant expression, not the result of a value that could only be computed at runtime.

Example:
```
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```
constants are valid for the entire time a program runs, within the scope in which they were declared.
This property makes it useful for values in our application domain that multiple parts of the program might need to know about,
such as the no. of points any player of a game is allowed to earn, or the speed of light.

## Shadowing
Rust allows us to declare a new variable with the same name as a previous variable.
Rustaceans say that the 1st variable is *shadowed* by the 2nd, which means that the 2nd variable is what the compiler will see
when that variable name is used.
In effect, the 2nd variable overshadows the 1st, taking any uses of the variable name to itself until either it itself is shadowed
or the scope ends.
We can shadow a variable by using the same variable's name and repeating the use of the `let` keyword as follows:
```rust
fn main(){
  let x = 5;
  
  let x = x + 1;

  {
    let x = x * 2;
    println!("The value of x in the inner scope is: {x}");
  }

  println!("The value of x is: {x}");
}
```
This program, 1st binds x to a value of 5.
Then, it creates a new variable x by repeating `let x=`, taking the original value and adding 1 so that the value of x is now 6.
Now, within an inner scope created using the curly brackets, the 3rd let statement also shadows `x` and creates a new variable,
multiplying the previous value by 2 to give x a value of 12.
When that scope is over, the inner shadowing ends and x returns to being 6.
Therefore the output would be:
The value of x in the inner scope is: 12
The value of x is: 6

Shadowing is different from marking a variable as `mut` because we'll get a compile-time error if we accidentally try to reassign
to this variable without using the keyword `let`.
By using `let` we can perform a few transformations on a value but have the variable be immutable after those transformations
are completed.
Another difference b/w `mut` and shadowing is that because we're effectively creating a new variable when we are using the `let` keyword
again, we can change the type of the value but reuse the same name.
Example:
```
let spaces = "    ";
let spaces = spaces.len();
```

The 1st `spaces` variable is a string type, the second `spaces` variable is a number type.
However if we tried to use `mut` in this case, then we will get a compile-time error:
```
let mut spaces = "    ";
spaces = spaces.len();
```

It will return a mismatched types error.
