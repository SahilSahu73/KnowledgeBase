"""
## Problem 7
You are given a string s consisting of lowercase letters and parentheses '(' and ')'.
Remove the minimum number of parentheses so that the resulting string is a valid parentheses string. Return any valid result.

A string is valid if:

Parentheses are balanced

Every opening parenthesis has a matching closing parenthesis in the correct order

```
Input: s = "lee(t(c)o)de)"
Output: "lee(t(c)o)de"

Input: s = "a)b(c)d"
Output: "ab(c)d"

Input: s = "))(("
Output: ""
"""


def paranthesis(s: str) -> str:
    stack = []
    candidates = []
    s_list = list(s)
    for i in range(len(s_list)):
        if s_list[i] == "(":
            stack.append(i)
        elif s_list[i] == ")":
            if len(stack) > 0:
                stack.pop()
                continue
            else:
                candidates.append(i)
    if len(stack) > 0:
        candidates.extend(stack)
    print(candidates)
    # Delete in reverse order
    for index in sorted(candidates, reverse=True):
        del s_list[index]

    return "".join(s_list)


if __name__ == "__main__":
    test_str = "lee(t(c)o)de)"
    test_2 = "a)b(c)d"
    test_3 = "))(("
    sol = paranthesis(test_3)
    print(sol)
