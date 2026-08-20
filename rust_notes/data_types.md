# Data Types

Every value is of a certain data type - tells rust how to deal with that data.
Rust is a *Statically typed language* - means that it must know the types of all variables at compile-time.
The compiler can usually infer what type we want to use based on the value and how we use it.
In cases when many types are possible, we must add a type annotation:
```rust
let guess: u32 = "42".parse().expect("Not a number!");
```
If we don't add the u32 type annotation above then rust will show an error as there are multiple data types possible for
data parsed and compiler needs an exact type.

## Scalar Types
- represents a single value.
- 4 types: integers, floating-point numbers, boolean and characters

### Interger Types
- numbers without a fractional component
- They can be signed or unsigned and should have an explicit size.
- signed - number with a sign (basically has a posibility of being a negative number)
- unsigned - numbers that does not require a sign, i.e. only positive numbers.

signed numbers are stored using 2's complement representation.
Each signed variant can store numbers from -(2^n-1) to 2^n-1 - 1 inclusive, where n is the number of bits
`i8` can store numbers from -(2)^7 to 2^7 - 1 = -128 to 127
unsigned can store (i.e. `u8`) from 0 to 2^8 - 1 = 0 to 255

| Length | Signed | Unsigned |
| --------------- | --------------- | --------------- |
| 8-bit | `i8` | `u8` |
| 16-bit | `i16` | `u16` |
| 32-bit | `i32` | `u32` |
| 64-bit | `i64` | `u64` |
| 128-bit | `i128` | `u128` |

- `isize` and `usize` - depends on the architecture the computer is running on: 64 bits if on a 64-bit architecture and 32 bits if on other.
Interger types default to `i32`
primary situation in which you'd have to use `isize` or `usize` is when indexing some sort of collection.

### Interger Overflow
Lets say we have a variable of type `u8` - can hold values between 0 to 255
If we try to store maybe 256 or any greater number in this variable then *integer overflow* will occur, which can result  in 2 behaviors.
When compiling in debug, rust has checks for integer overflow that cause the program to *panic* at runtime if this behavior occurs.

> [!NOTE]
> Rust uses the term *panicking* when a program exits with an error. (more in chp 9)

When compiling in release mode with the `--release` flag, rust does not include checks for integer overflow that causes panics.
Instead, if overflow occurs, rust performs 2's complements wrapping, in short, values greater than the maximum value the type can hold
"wrap around" to the minimum of the values the type can hold.
In case of a `u8`, value 256 becomes 0, 257 becomes 1, and so on....
Program won't panic, but the variables will have value that you were not expecting.
Relying on integer overflow's wrapping behavior is considered an error.

> [!NOTE]
> To explicitly handle the possibility of overflow, we can use these families of methods provided by the standard library for the primitive
> numeric types:
> - wrap in all modes with the `wrapping_*` methods, such as `wrapping_add`.
> - Return the `None` value if there is an overflow with the `checked_*` methods.
> - Return the value and a Boolean indicating whether there was overflow with the `overflowing_*` methods.
> - Saturate at the value's minimum or maximum values with the `saturating_*` methods.

### Floating-Point Types
- Only two types for storing numbers with decimal points.
- `f32` and `f64`, which are 32-bits and 64-bits in size.
- default to `f64` - has roughly same speed as `f32` but is capable of more precision on modern CPUs.
- All floating-point types are signed.

```rust
fn main(){
    let x = 3.0;  // f64

    let y: f32 = 3.0;  // f32
}
```

### Numeric Operations
- Integer division truncates towards 0 to the nearest integer.
example: let truncated = -5 / 3;
returns: -1

rest all operations works as expected.

### Boolean Type
2 possible values: `true` and `false`
- booleans are 1 byte in size.
- type is specified using `bool`.

### The Character Type
- represent char with single quotation marks
- whereas strings with double quotation marks.
- `char` type is 4 byte is size and represents a unicode scalar value, means it can represent a lot more than just ASCII.


## Compound Types
- allows to group multiple types into 1 type.
- 2 primitive compound types: arrays and tuples

### Tuple Type
- general way of grouping together no. of values with variety of types into one compound type.
- Tuples have **fixed length**: once declared, they cannot grow or shrink in size.

- comma-separated list of values inside parentheses.
Each position has a type, and types of the different values in the tuple don't have to be same.

```rust
fn main(){
    let tup: (i32, f64, u8) = (-69, 3.0, 1);
}
```
`tup` variable binds to the entire tuple because it is considered a single compound element.
To get individual values out of tuple, use pattern matching to destructure a tuple value.
```rust
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is {y}.");
}
```
This is called destructuring.
Can also access individual elements using the `.`
example: in the above code y = tup.1
would hold the value 6.4

- Tuple without any values are called *unit*.
This value and its corresponding type are both written `()`, and represent an empty value or an empty return type.

### Array Type
- Every element of array must be of same type.
- Array in rust have fixed length.
- written as comma-separated values inside square brackets:
```rust
fn main() {
    let a = [1,2,3,4];
    let b: [i32; 5] = [1,2,3,4,5];
    let c = [3; 5];  // will have [3,3,3,3,3]
}
```
- useful when we want the data to be allocated on the stack and not the heap, or when we want to ensure that we always will have a
fixed number of elements.
- Vector is a similar collection type provided by the standard library that is allowed to grow or shrink in size because it's contents
live on a heap.
- element access => `let first = a[0];`
- In case of entering an index more than or equal to the lenght of the array, the program will exit with an error.
