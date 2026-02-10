# Lesson 1
- **GO** is a compile time language

To compile a go file:
> go build greet.go

```go

package main
import "fmt"

func main(){
  fmt.Println("Hello World")
}
```

It compiles the file and creates an executable file.
Which then can be executed by:
> ./greet

The problem here now is that we have to compile it each time we make a change and 
create an executable file which is tedious and difficult to track.

We have another command that will directly execute the file.
> go run greet.go

Projects contains many `.go` files, organized into packages.
Mentioning `package main` indicates that the current file belongs to the package main.
Each package is like a directory.
