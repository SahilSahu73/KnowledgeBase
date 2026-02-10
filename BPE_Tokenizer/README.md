# Intro
Main idea is to convert the strings to integers so that we can have a lookup of each string and pass the 
corresponding vector embedding to the Model.

To the Text into the Transformers:
We know that strings are immutable sequences of Unicode code points.
(The unicode standard is a text encoding standard.)
Basically a list of all the character (including emoji's) what they look like and what integers represent
those characters.
We can access this standard using the `ord()` function in python.
It returns the integer that corresponds to the passed character.
e.g. `ord("h")` => 104  (ASCII Values)

The main problem that the tokenizer solves is the sequence length.
Now, if we directly try to pass the ASCII values, i.e. integers of each character in the string, then our 
vocabulary remains fixed and small and the sequence that the Transformers can accept will become very long which
will exceed the limit due to computational constraints.
Through Byte-Pair encoding we are trying to compress the total sequence length and find a sweet spot for the
sequence compression and the vocabulary length.

Tokenization Issues in LLMs - Why you should care:
- Why can’t LLM spell words? Tokenization.
- Why can’t LLM do string processing tasks like reversing a string? Tokenization.
- Why is LLM bad at non-English languages? Tokenization.
- Why is LLM bad at simple arithmetic? Tokenization.
- Why did GPT-2 have more than necessary trouble coding in Python? Tokenization.
- Why did my LLM abruptly halt when it sees the string “<|endoftext|>”? Tokenization.
- Why should I prefer YAML over JSON with LLMs? Tokenization.
- What is the root of suffering? Tokenization.
