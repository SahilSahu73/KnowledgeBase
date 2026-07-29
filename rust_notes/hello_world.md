we wrote a small hello world program.
```rust
fn main(){
  println!("Hello, World!");
}
```
We defined a function named `main()`.
Special function - always the first code that runs in every executable rust program.
Here the main() function has no parameters and returns nothing
The function body is wrapped in `{}` - required around all function bodies.

The body does 1 work - print the hello world.
Important things to note:
1. `println!` calls a Rust macro. If it had called a function instead, it would be entered as `println` (without the `!`).
Rust macros are a way to write code that generates code to extend Rust syntax - more detail in Chapter 20.
So using an `!` means that we're calling a macro instead of a normal function and that macros don't always follow the
same rules as functions.

2. "Hello, World!" string is passed as an argument to `println!`, and the string is printed to screen.

3. We end the line with a `;` which indicates that the expression is over, and the next line is ready to begin.

---

Before running a program, compile it first using the rust compiler.
> rustc main.rs

similar to how things were done in C or C++.
After compiling successfully, rust outputs a binary executable.

Rust is an *ahead-of-time compiled* language, meaning you can compile a program and give the executable to someone else,
and they can run it even without having rust installed.
