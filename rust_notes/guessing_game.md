# Guessing Game

## Setting up a New Project
> cargo new guessing_game
> cd guessing_game

## Processing a Guess
1st part of this program is to ask for user input, process that input and check that the input is in the expected format.
```rust
use std::io;

fn main(){
    println!("Guessing Game !!");

    println!("Please input your guess: ");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to real line.");

    println!("Your guess: {guess}");
}
```
- To obtain user input and then print the result as output, we need `io` input/output library, and added it in the scope.
The `io` library comes from the standard library - `std`
- By default, rust has a set of items defined in the standard library that it brings into the scope of every program.
This set is called the *prelude*.
- Rust comes with a variety of things in its standard library. However, if you had to manually import every single thing that you used,
it would be very verbose. But importing a lot of things that a program never uses isn’t good either. A balance needs to be struck.
The prelude is the list of things that Rust automatically imports into every Rust program. It’s kept as small as possible, and is 
focused on things, particularly traits, which are used in almost every single Rust program.
- If a type you want to use isn't in the prelude, you have to bring that type into scope explicitly with a `use` statement.
- The initial 2 println! statements print the given text on the screen.
- `let mut guess` introduces a mutable variable, the `=` tells rust, we want to bind something/value to this variable.
In this case the variable `guess` is bound to the result of calling the function `String::new`. It is a function that returns a
new instance of `String`. `String` is a string type provided by the standard library that is growable, UTF-8 encoded bit of text.
The `::` syntax in the `::new` line indicates that new is an associated function of the String type.
An *associated function* is a function that's implemented on a type, in this case `String`.
This `new` function creates a new, empty string.
Basically the full line has created a mutable variable that is currently bound to a new, empty instance of string.
- The next line imports the `stdin` function from the `io` module - to handle user input:
```
io::stdin().read_line(&mut guess).expect("Failed to real line.")
```
The `stdin()` function returns an instance of `std::io::Stdin` - type that represents a handle to the standard input for your terminal.
We are passing the `&mut guess` as an argument to the read_line() method to get input from the user and store in it.
The full job of `read_line()` is to take whatever the user types into standard input and append that into a string (without overwriting
its contents), so we therefore pass that string as an argument. The string argument has to be mutable, so that the method can change the
contents of the string.
The `&` indicates that this argument is a *reference*. References are also immutable by default.
`read_line` puts whatever the user enters into the string we pass it to, but it also returns a `Result` value.
`Result` is an `enumeration`, aka `enum` - type that can in one of multiple possible states, each possible state a *variant*.
Purpose of these `Result` types is to encode error-handling information.
`Result`'s variants are `ok` and `Err`.
`ok` - indicates operation was successful, and it contains the successfully generated value.
`Err` - means the operation failed, and contains the info. about how or why the operation failed.

Values of the `Result` type, have methods defined on them (like values of any type).
Instance of Result - has an `expect` method that we can call.
If instance of `Result` is an `Err` value - `expect` will cause program to crash - display the message that was passed as an arg to `expect`.
If `ok` then expect will take the return value that `ok` is holding and return just that value to us so that we can use it.
Now if we do not use `expect`, the program will compile but give a warning - unused `Result` that must be used.

## Generating a Secret Number
The project that we are building is a binary crate, which is an executable.
The `rand` crate is a library crate, which contains code that is intended to be used in other programs and cant be executed on its own.
Cargo's coordination of external crates is where Cargo shines. Before we can write code that uses `rand` crate, *Cargo.toml* needs to
include the `rand` crate as a dependency.
```rust
use std::io;
use rand::Rng;

fn main(){
    println!("");

    let secret_num = rand::thread_rng().gen_range(1..=100);

    println!("The secret_num generated: {secret_num}");
    println!("");

    let mut guess = String::new();

    io::stdin()
      .read_line(&mut guess)
      .expect("Failed to read line.");

    println!("You guessed: {guess}");
}
```
We added `use rand::Rng` - `Rng` trait defines methods that random number generators implement, and this trait must be in scope for us
to use those methods.
`rand::thread_rng` function - random number generator - local to the current thread of execution and is seeded by the OS.
Then the gen_range() method is called on the random num generator - this method is defined by the `Rng` trait - takes a range expression
in the form `start..=end` as argument - lower and upper bound inclusive - and generates a random num in that range.

> [!NOTE]
> We wont know which traits to use or which methods and functions to call from a crate, so each crate has its own documentation with instructions for using it. Running `cargo doc --open` will build documentation provided by all the dependencies locally and open it in the browser.

## Comparing the guess to the secret_num
```rust
use std::io;
use rand::Rng;

use std::cmp::Ordering;

fn main(){
    // previous same code as above
    println!("Your guess: {guess}");

    match guess.cmp(&secret_num) {
        Ordering::Less => println!("Too small"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You Win!!!!"),
    }
}
```

