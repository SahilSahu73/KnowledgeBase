# Cargo
Cargo is Rust's build system and package manager.
Mostly this tool is used to manage rust projects because it handles alot of tasks for us, such as building your code,
downloading the libraries your code depends upon, and building those libraries (dependencies).

## Creating a project with Cargo
Command to create a project using cargo
> cargo new hello_cargo

This creates a new directory and project. Project name we kept was hello_cargo so accordingly it created a project folder.
Cargo creates its files in a directory of the same name.

Cargo generated 2 files:
Cargo.toml file and a `src` directory with main.rs file inside.

Cargo also initialized a new Git repository along with a `.gitignore` file. Git won't be generated if you run `cargo new` within an
existing git repository; can override this behaviour by using `cargo new --vcs=git`

### Cargo.toml file
TOML - Tom's Obvious, Minimal Language format
In the .toml file created the 1st line we see `[package]`, it is a section heading that indicates that the following statements
are configuring a package.
The next following lines set the configuration information Cargo needs to compile your program: the name, the version, and
the edition of rust to use.

the last line `[dependencies]`, is the start of a section for us to list any of the project's dependencies.
In Rust, packages of code are referred to as *crates*.

Cargo expects our source files to live inside the `src` directory.
Usual convention of project repositories, is that the top-level project directory is just for README files, license info,
configuration files, and anything else not related to your code.
Cargo helps us organize our projects.

> cargo init

running this line initializes the project and creates the Cargo.toml file for us automatically.

### Building and running a Cargo project

> cargo build

This command creates an executable file in `target/debug/hello_cargo` rather than in the cwd.
Because the default build is a debug build, Cargo puts the binary in a directory named *debug*.
Run the executable using this command:
> ./target/debug/hello_cargo

Running `cargo build` for the 1st time - creates a new file at the top level - `Cargo.lock`
It keeps track of the exact version of the dependencies in our project.
No need to manually manage this file, cargo manages its contents.

Can also use:
> cargo run

It compiles the code and runs the resultant executable all in one command.
More convenient

Another command:
> cargo check

It quickly checks the code to make sure it compiles but doesn't produce an executable.
Often cargo check is faster than cargo build because it skips the step of producing an executable.

### Building for Release
When your project is ready for release, we can use `cargo build --release` to compile it with optimizations.
This command will create an executable in `target/release`.
Optimizations make the code run faster, but turning them on lengthens the time it takes for the program to compile.
Thats why there are 2 different profiles: one for development - when we want to rebuild quickly and often, and another for
building the final program you'll give to a user that won't be rebuilt repeatedly and that will run as fast as possible.
